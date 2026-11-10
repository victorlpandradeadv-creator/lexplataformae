# Instructions for each translator

You translate one batch of the Portuguese site lexplataformae.com.br into English. The site adapts a Brazilian doctoral thesis in law (consumer law, digital platforms) for three readers. Information (lay consumers), Doctrine (lawyers), Science (scholars, with literal thesis text). Pages under tese/ are the thesis full text itself.

Before translating, read traducao/glossario.md in full and follow it strictly. Consistency across batches depends on it.

## How to work

1. Get the next segments.
   python3 ferramentas/en/gravar.py LOTE --faltam 50
   Each line is {"k", "pagina", "pt"}. The page path tells you the context (caminho/ and problemas/ are lay text, doutrina/ is for lawyers, tese/ is the thesis).
2. Translate them and save in one command, one JSON object per line, with a quoted heredoc so nothing is interpreted.
   python3 ferramentas/en/gravar.py LOTE <<'JSONL'
   {"k": "...", "en": "..."}
   JSONL
   JSON strings must escape double quotes as \" and backslashes as \\. Typographic quotes “ ” need no escaping.
3. Read the report. Fix and resend any refused line. Repeat until it says faltam 0.

## Rules for each segment

- Numbered markers like <1>, </1>, <2/> stand for HTML tags. Keep every marker exactly, the same set, properly nested. Move them only as far as English word order requires. Never add, drop or renumber a marker.
- Translate meaning faithfully. Do not summarize, expand, explain or add anything. Do not drop caveats or modal verbs.
- Literal thesis passages (they often appear between quotation marks, or the segment is a full sentence from the thesis followed by a page reference such as p. 412) are translated faithfully and keep the thesis's punctuation.
- Site prose follows the glossary style rules (no semicolons, colons or dashes).
- Keep page references (p. 12, p. 401-403), section numbers (7.1.2), article numbers, URLs, proper names, song and game titles unchanged.
- Bibliographic references stay in Portuguese, per the glossary.
- If a segment needs no translation (a name, a number, a URL, a reference entry), send it back unchanged.
- HTML entities like &amp; or &lt; stay as entities.
- Short labels (menu items, buttons) use the glossary forms.

When the batch is complete, reply with one line. The batch name, the count, and at most three real translation dilemmas you met that the glossary does not settle, each in one sentence with the Portuguese term. Do not report anything else.
