# Instructions for each English reviewer

You review one batch of the English version of lexplataformae.com.br, a site that adapts a Brazilian doctoral thesis in consumer law and digital platforms. The translation is complete. Your job is to make the English credible, reliable and fluent, the way a careful native editor at a good law review or a serious public-interest publication would leave it. You are not retranslating from scratch.

Read traducao/glossario.md first. Glossary terms are fixed. Do not change them.

## How to work

1. python3 ferramentas/en/revisar.py LOTE --proximos 40
   Each line has k, pagina, pt (the Portuguese source) and en (the current English).
2. For each segment decide. If the English already reads well and says exactly what the Portuguese says, leave it. If not, rewrite it.
3. Send only the rewritten ones, one JSON per line, with a quoted heredoc.
   python3 ferramentas/en/revisar.py LOTE <<'JSONL'
   {"k": "...", "en": "..."}
   JSONL
4. Mark the untouched ones as reviewed.
   python3 ferramentas/en/revisar.py LOTE --vistos k1 k2 k3 ...
5. Repeat until it reports faltam 0.

## What to fix

- Calques of Portuguese syntax. Subject placed late, chains of "of the ... of the", needless nominalizations ("the realization of the analysis"), sentences that open with "It is" or "There is" for no reason, adjectives stacked after nouns.
- False friends and wrong register. actually, eventually, pretend, realize, attend, intend, sensible, sympathetic, effectively, punctual, in the sense that, at the level of, in terms of, the same (as a pronoun), properly said, among others.
- Prepositions and articles that a native would not use. Missing or extra "the".
- Cadence. Vary sentence openings. Join choppy sentences where the Portuguese joins them, split where English needs air. Keep rhythm natural when read aloud.
- Idiom. Prefer the expression an English-speaking lawyer or journalist would actually use, as long as the meaning stays exact.
- Consistency of terms inside the segment and with the glossary.

## What must not change

- Meaning. Every claim, condition, modal verb and caveat stays (may, can, possibly, in principle). Never upgrade a possibility into a certainty. Never conclude that a company is abusive.
- Numbered markers like <1>, </1>, <2/>. Same set, properly nested.
- Page references, section numbers, article numbers, names, titles, URLs, bibliographic references.
- Site prose (everything outside tese/ pages that is not a literal thesis passage) uses no colons, no semicolons, no dashes. Keep it that way.
- Literal thesis passages and the thesis full text (pages under tese/) keep the thesis's punctuation and structure as far as English allows. Improve fluency there only by word choice and word order, not by restructuring the argument.
- Lay pages (caminho/, problemas/, direitos/, como-reclamar/, the home page) speak to an ordinary consumer in the second person. Plain, warm, direct. No legal jargon left unexplained.
- Doctrine pages (doutrina/, roteiro/, conceitos/) speak to lawyers. Precise and didactic.

When the batch is complete, reply with one line. The batch name, how many segments you rewrote, and at most two recurring problems you saw.

## Strict reading rule (second round, 10/11/2026)

Read every segment in full, one by one, against its Portuguese. Never mark a segment as reviewed without reading it, never sample, never bulk-mark. Your batch is small on purpose (about 120 segments). If a segment repeats one you already handled in this batch, apply the same decision. Report the exact number you read and the number you rewrote.

## Thesis full text (batches named tese-rNN)

These pages are the thesis itself, in a machine translation that the site labels as not reviewed by the author. Make it read like a careful academic translation into English. Keep the thesis's own punctuation, paragraphing, argument order and every footnote reference. Fix calques, false friends, articles, prepositions, word order and terminology against the glossary. Never summarize, never drop a clause, never soften or strengthen a claim. Quotations the thesis gives in English or Spanish stay as they are. Bibliographic entries stay in Portuguese.

If the tool output is cut off because segments are long, ask for fewer at a time (--proximos 10 or even 3). Never mark a segment you could not read in full.
