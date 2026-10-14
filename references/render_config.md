# Render Configuration

## One layout, two files

The DOCX is the single definition of the document's layout. The PDF is exported from that DOCX. There is no second styling system to keep in sync, and the PDF you submit is exactly what the DOCX looks like.

```
resume.md  ->  DOCX  ->  PDF
             (layout)  (export)
```

This also means the DOCX can be edited by hand. Open it in Word or Google Docs, change what you like, then re-export the PDF from it with `--from-docx`.

## Theme keys (`profile.yaml: render`)
| Key | Default | Meaning |
|---|---|---|
| page_size | A4 | A4 or Letter |
| margins_mm | [16, 14, 16, 14] | top, right, bottom, left |
| font_family | Segoe UI, Calibri, Arial, sans-serif | the first name in the list is used |
| body_pt | 10 | body font size |
| line_spacing | 1.25 | line height multiplier |
| para_after_pt | 6 | space after paragraphs |
| accent | #0284c7 | header rule and links |
| heading_colour | #0369a1 | section headings |
| text_colour | #1e293b | body text |
| filename_pattern | {name} - {company} - {position} {doc} | `{doc}` becomes CV or Cover Letter |

Change a value here and both files change together, because the PDF comes from the DOCX.

## PDF engines

Tried in this order. `python scripts/render_pdf.py` prints what your machine has.

1. **Microsoft Word** through COM, on Windows with `pywin32` installed. Word is the reference renderer for `.docx`, so a document you edited in Word exports exactly as it looked. It runs a private Word instance, so your open Word session is untouched.
2. **LibreOffice** headless. Cross-platform and free. It uses a private profile directory, so it works even when LibreOffice is already open.
3. **Headless Chromium**, opt-in only with `--html-pdf`. This one does not read the DOCX at all; it renders separate HTML, so the result will not match the DOCX. Use it only when neither converter can be installed.

Force one with `CV_PDF_ENGINE=word|libreoffice|browser`. Point `CV_BROWSER` at a browser binary for the escape hatch.

If no converter is found, the DOCX is still written and the render prints instructions. You can always export a PDF from Word or LibreOffice yourself.

## Editing after render

* **Edit `resume.md`**, then re-run the render. Both files are rebuilt. This is the normal path.
* **Edit the DOCX by hand**, then run the render with `--from-docx`. Only the PDF is rebuilt, from your edited DOCX. The markdown is left alone and `metadata.json` records that the DOCX is now the source of truth. A later rebuild from markdown would overwrite your hand edits, so fold them back into `resume.md` when you can.

With Word, close the document before exporting, or the export uses the last saved version.

## Page limits

`render_cv.py` prints `PAGES: n (limit m, market X)` and exits with code 2 when n exceeds the market's `page_limit`. The count comes from the exported PDF, so it reflects the real document. Treat exit 2 as "run a brevity pass and re-render".

## File size and emoji

Avoid colour emoji in documents. A single emoji makes Word embed the whole colour emoji font, which took one example cover letter from 78 KB to 3.9 MB. Many application portals cap uploads at 2 MB. The default cover letter marker is therefore a plain check mark (U+2713), not the emoji one, and it looks more formal in print. The same applies to any emoji a user asks for in a bullet.

## Market selection

`resume.md` frontmatter `market:` first, then `--market`, then `metadata.json`, then the first market in the profile.

## Debugging

`--dry-run` prints the parsed structure without rendering. `--docx-only` skips the PDF. `--pdf-only` produces just the PDF (the DOCX is built as an intermediate and removed).
