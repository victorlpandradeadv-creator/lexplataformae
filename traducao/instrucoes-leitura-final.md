# Final reading of the English site (12/11/2026)

The author asked for every page of the English site to be read and corrected. You have one batch, traducao/revisao/lotes/LOTE.json, holding the unique segments of a group of pages, in page order.

1. Read traducao/glossario.md and traducao/instrucoes-revisor.md first. Their rules apply. Notes from 11/11 and 12/11/2026 that override older text there:
   - The third mode is Scholarship (never Science). Para operar is In practice. Caminho is Path. OIC is IOC.
   - The long form "Immaterial Object of Consumption" appears once per page where the category is introduced. Elsewhere use IOC, or lowercase when applied to a concrete thing.
   - Brazilian law must be recognizable at key moments. The site does not claim the thesis holds in other legal systems.
   - Singular they for the generic consumer. "my child", never "son or daughter".
   - Site prose uses no colons, semicolons or dashes. Literal thesis passages keep their punctuation.
2. Work with python3 ferramentas/en/revisar.py traducao/revisao/lotes/LOTE.json --proximos 30 (fewer if output is cut). Read every segment in full against its Portuguese. Rewrite only what is wrong, unclear, unnatural, inconsistent or still in Portuguese. Bibliographic references stay as they are. Literal quotations in a foreign language other than Portuguese stay as they are.
3. Send rewrites through revisar.py with a quoted heredoc. Keep numbered markers identical. Mark the rest with --vistos. Never bulk-mark unread segments.
4. Do not run gerar_site.py, lotes.py or any git command.

Reply in English, briefly. Segments read, segments rewritten, and up to three examples before and after.
