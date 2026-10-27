"""Gera dados/atlas.json a partir das fichas conferidas e monta o protótipo.

Uso
    python3 ferramentas/gerar_dados.py

Lê conceitos/ficha-canonica-v0.md e conceitos/percursos.md, que são a fonte
de verdade do conteúdo. Nenhum texto citado é escrito à mão no site. Tudo vem
destes arquivos, já conferidos por ferramentas/conferir_citacoes.py.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FICHA = RAIZ / "conceitos" / "ficha-canonica-v0.md"
PERCURSOS = RAIZ / "conceitos" / "percursos.md"
SAIDA = RAIZ / "dados" / "atlas.json"
MODELO = RAIZ / "prototipo" / "modelo.html"
PAGINA = RAIZ / "prototipo" / "index.html"
EPIGRAFES = RAIZ / "dados" / "epigrafes.json"

# Identificadores estáveis de cada conceito, na ordem da ficha.
SLUGS = {
    "Lex Plataformae": "lex-plataformae",
    "Objeto Imaterial de Consumo (OIC)": "oic",
    "Vulnerabilidade semiótica": "vulnerabilidade-semiotica",
    "Antecipação hipercuratorial": "antecipacao-hipercuratorial",
    "Teleologia abusiva": "teleologia-abusiva",
    "Auditabilidade aberta": "auditabilidade-aberta",
    "Equivalência de valor funcional": "equivalencia-de-valor-funcional",
    "Função social da propriedade intelectual": "funcao-social-da-pi",
    "Recomposição funcional e correção de regime": "recomposicao-funcional",
    "Feixe de fruição governada": "feixe-de-fruicao-governada",
    "Ilícito de arquitetura": "ilicito-de-arquitetura",
    "Integridade pessoal": "integridade-pessoal",
}

# Os nove conceitos não são numerados. São independentes e, sob o OIC, funcionam
# de forma integrada (nota do autor, 26/10/2026). O OIC é o eixo de integração.
EIXO = "oic"

# Pares que aparecem colados nos percursos.
# OIC e feixe são gêmeos por decisão do autor em 26/10/2026.
# Teleologia abusiva e ilícito de arquitetura andam juntos em todos os títulos da tese (5.1.3, 6.4, 7.1.1.7).
PARES = {
    "oic": ("feixe-de-fruicao-governada", "gêmeos"),
    "teleologia-abusiva": ("ilicito-de-arquitetura", "par"),
}

# Seção do 7.1.1 de cada conceito que saiu do Atlas e segue no Roteiro.
SECAO_ROTEIRO = {"funcao-social-da-pi": "7.1.1.9", "recomposicao-funcional": "7.1.1.10"}


def par_de(cid):
    if cid in PARES:
        return {"id": PARES[cid][0], "rotulo": PARES[cid][1]}
    for k, (outro, rotulo) in PARES.items():
        if outro == cid:
            return {"id": k, "rotulo": rotulo}
    return None

# Passos dos percursos que não são conceitos do Atlas.
PASSOS = {
    "dever-de-informar": {"nome": "Dever de informar", "secao": "7.1.1.3", "tipo": "roteiro"},
    "publicidade-e-oferta": {"nome": "Publicidade e oferta", "secao": "7.1.1.4", "tipo": "roteiro"},
    "prova-e-onus": {"nome": "Prova e ônus", "secao": "7.1.1.8", "tipo": "roteiro"},
}

# Ordem e papel de cada conceito em cada percurso. Os papéis seguem de perto
# o texto da página indicada em "fonte" e não atribuem nada que a tese não diga.
PERCURSOS_DEF = {
    "consumidor": {
        "nome": "Percurso do consumidor",
        "onde": "5.1",
        "fonte": "p. 394-395",
        "logica": "Expõe os conceitos a partir da posição de quem consome.",
        "sequencia": [
            ("vulnerabilidade-semiotica", "descreve a condição"),
            ("oic", "descreve o objeto"),
            ("teleologia-abusiva", "descreve o ilícito"),
            ("integridade-pessoal", "descreve os bens protegidos"),  # camada de bens protegidos, fora do Atlas
            ("auditabilidade-aberta", "critério operacional de verificação e recomposição"),
            ("equivalencia-de-valor-funcional", "critério operacional de verificação e recomposição"),
        ],
    },
    "julgador": {
        "nome": "Percurso do julgador",
        "onde": "7.1.1",
        "fonte": "p. 716-717",
        "logica": "Decide passo a passo. Cada parâmetro prepara o seguinte.",
        "sequencia": [
            ("oic", "qualificação do objeto e do regime de fruição"),
            ("vulnerabilidade-semiotica", "governança do sentido e da inteligibilidade do vínculo"),
            ("dever-de-informar", "organização da expectativa, da escolha e da contestação"),
            ("publicidade-e-oferta", "organização da expectativa, da escolha e da contestação"),
            ("auditabilidade-aberta", "critério de verificação, contenção e imputação"),
            ("equivalencia-de-valor-funcional", "critério de verificação, contenção e imputação"),
            ("teleologia-abusiva", "critério de verificação, contenção e imputação"),
            ("prova-e-onus", "critério de verificação, contenção e imputação"),
            ("funcao-social-da-pi", "fecho operacional. Limite da exclusividade privada"),
            ("recomposicao-funcional", "fecho operacional. Forma adequada de resposta ao conflito"),
        ],
    },
    "regime": {
        "nome": "Percurso do regime",
        "onde": "Conclusão",
        "fonte": "p. 800",
        "logica": "Resume o regime inteiro numa frase, conceito por conceito.",
        "sequencia": [
            ("oic", "qualifica o produto imaterial"),
            ("vulnerabilidade-semiotica", "localiza a assimetria relevante"),
            ("antecipacao-hipercuratorial", "lê a expectativa governada"),
            ("teleologia-abusiva", "identifica o ilícito"),
            ("auditabilidade-aberta", "controla as alterações"),
            ("equivalencia-de-valor-funcional", "controla as alterações"),
            ("funcao-social-da-pi", "contém a exclusividade"),
            ("recomposicao-funcional", "reorganiza os remédios"),
        ],
    },
}

CITACAO = re.compile(r"^> (.+?) \((p\. [\d\-]+|Resumo)\)\s*$")
ROTULO = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$")


def ler_ficha():
    texto = FICHA.read_text(encoding="utf-8")
    conceitos = []
    for bloco in re.split(r"^## ", texto, flags=re.M)[1:]:
        linhas = bloco.split("\n")
        titulo = linhas[0].strip()
        numerado = re.match(r"^Conceito\. (.+)$", titulo)
        roteiro = re.match(r"^Roteiro\. (.+)$", titulo)
        bens = re.match(r"^Bens protegidos\. (.+)$", titulo)
        if numerado:
            nome, tipo = numerado.group(1), "conceito"
        elif roteiro:
            nome, tipo = roteiro.group(1), "roteiro"
        elif bens:
            nome, tipo = bens.group(1), "bens"
        else:
            continue
        campos, atual = [], None
        for linha in linhas[1:]:
            linha = linha.rstrip()
            if not linha or linha == "---":
                continue
            m = ROTULO.match(linha)
            if m:
                rotulo = m.group(1).rstrip(".")
                atual = {"rotulo": rotulo, "texto": m.group(2).strip(), "citacoes": []}
                campos.append(atual)
                continue
            c = CITACAO.match(linha)
            if c and atual is not None:
                atual["citacoes"].append({"texto": c.group(1), "ref": c.group(2)})
            elif atual is not None:
                atual["texto"] = (atual["texto"] + " " + linha).strip()
        conceitos.append({
            "id": SLUGS[nome],
            "nome": nome,
            "tipo": tipo,
            "eixo": SLUGS[nome] == EIXO,
            "par": par_de(SLUGS[nome]),
            "secao": SECAO_ROTEIRO.get(SLUGS[nome]),
            "campos": campos,
        })
    return conceitos


def ler_percursos():
    texto = PERCURSOS.read_text(encoding="utf-8")
    trechos = {}
    for bloco in re.split(r"^## ", texto, flags=re.M)[1:]:
        chave = bloco.split("\n")[0].strip()
        for linha in bloco.split("\n")[1:]:
            c = CITACAO.match(linha)
            if c:
                trechos[chave] = {"texto": c.group(1), "ref": c.group(2)}
    return trechos


def main():
    conceitos = ler_ficha()
    trechos = ler_percursos()
    ids = {c["id"] for c in conceitos} | set(PASSOS)
    percursos = {}
    for chave, p in PERCURSOS_DEF.items():
        for item, _ in p["sequencia"]:
            assert item in ids, f"conceito desconhecido no percurso {chave}: {item}"
        percursos[chave] = {**p, "trecho": trechos[chave],
                            "sequencia": [{"id": i, "papel": papel, "par": (PARES[i][0] if i in PARES else None),
                                           "par_rotulo": (PARES[i][1] if i in PARES else None)} for i, papel in p["sequencia"]]}
    dados = {
        "versao": "v0",
        "abertura": trechos["abertura"],
        "conceitos": conceitos,
        "passos": PASSOS,
        "percursos": percursos,
        "epigrafes": json.loads(EPIGRAFES.read_text(encoding="utf-8")),
    }
    SAIDA.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    if MODELO.exists():
        embutido = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
        PAGINA.write_text(MODELO.read_text(encoding="utf-8").replace("__DADOS_ATLAS__", embutido), encoding="utf-8")
    print(f"{len(conceitos)} conceitos, {len(percursos)} percursos gravados em {SAIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
