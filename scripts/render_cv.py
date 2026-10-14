"""Render resume.md (and optionally cover_letter.md) to DOCX, then export the PDF from that DOCX.

The DOCX is the single definition of the layout. The PDF is exported from it, so the two always
match and a DOCX you edited by hand exports the PDF you expect.

Usage:
  python render_cv.py --resume <folder>/resume.md [--out-dir <folder>] [--data-dir D | --profile-dir P]
                      [--company X --position Y] [--market CODE] [--cover-letter]
                      [--docx-only | --pdf-only] [--from-docx] [--html-pdf] [--dry-run] [--tailoring]

  --from-docx   Do not rebuild from markdown. Export the PDF from the DOCX already in the folder.
                Use this after editing the DOCX by hand.
  --html-pdf    Escape hatch when no converter is installed. Builds the PDF from HTML instead of
                the DOCX, so it will not match the DOCX exactly.

Company, position and market come from resume.md frontmatter, then metadata.json, then the flags.
Prints one line per output plus "PAGES: n (limit m)". Exit 2 when the CV exceeds the page limit.
"""
import argparse
import glob
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from cv_parser import parse_markdown_cv, summary  # noqa: E402
from paths import load_profile  # noqa: E402
from render_common import theme_from_profile, pick_market, build_filename, display_name  # noqa: E402
import render_pdf  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def read_metadata(folder):
    path = os.path.join(folder, "metadata.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f), path
        except json.JSONDecodeError:
            return {}, path
    return {}, path


def write_metadata(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def pdf_from_docx(docx_path, pdf_path, result):
    ok, note = render_pdf.docx_to_pdf(docx_path, pdf_path)
    if ok:
        result["pdf"] = pdf_path
        result["pdf_engine"] = note
    else:
        result["pdf_error"] = note
        result["pdf_help"] = render_pdf.missing_converter_help()
    return result


def render_one(base_no_ext, out_dir, docx_fn, want_pdf, want_docx, html_fn=None, use_html_pdf=False):
    """Build the DOCX, then export the PDF from it. Returns the produced paths and any errors."""
    result = {}
    docx_path = os.path.join(out_dir, base_no_ext + ".docx")
    pdf_path = os.path.join(out_dir, base_no_ext + ".pdf")

    if use_html_pdf and want_pdf:
        html_path = os.path.join(out_dir, base_no_ext + ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_fn())
        ok, note = render_pdf.html_to_pdf(html_path, pdf_path)
        os.remove(html_path)
        if ok:
            result["pdf"] = pdf_path
            result["pdf_engine"] = note + " (from HTML; does not match the DOCX exactly)"
        else:
            result["pdf_error"] = note
        if not want_docx:
            return result

    # The DOCX is built whenever it is wanted, and also as the source for the PDF.
    need_docx_file = want_docx or (want_pdf and not use_html_pdf)
    if need_docx_file:
        try:
            docx_fn(docx_path)
            result["docx"] = docx_path
        except Exception as e:  # noqa: BLE001
            result["docx_error"] = str(e)
            if want_pdf and not use_html_pdf:
                result["pdf_error"] = "no DOCX to export from"
            return result

    if want_pdf and not use_html_pdf:
        pdf_from_docx(docx_path, pdf_path, result)

    if not want_docx and result.get("docx"):
        # --pdf-only: the DOCX was only a means to the PDF.
        os.remove(result.pop("docx"))
    return result


def locate_docx(out_dir, expected_base):
    """The DOCX to export from in --from-docx mode."""
    expected = os.path.join(out_dir, expected_base + ".docx")
    if os.path.exists(expected):
        return expected, None
    candidates = [p for p in glob.glob(os.path.join(out_dir, "*.docx"))
                  if not os.path.basename(p).startswith("~$") and "Cover Letter" not in os.path.basename(p)]
    if len(candidates) == 1:
        return candidates[0], None
    if not candidates:
        return None, "no DOCX found in " + out_dir + ". Render once without --from-docx first."
    return None, ("several DOCX files in " + out_dir + "; expected " + os.path.basename(expected) +
                  ". Rename the one you edited, or render without --from-docx.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--resume", required=True)
    ap.add_argument("--out-dir")
    ap.add_argument("--data-dir")
    ap.add_argument("--profile-dir")
    ap.add_argument("--company")
    ap.add_argument("--position")
    ap.add_argument("--market")
    ap.add_argument("--pdf-only", action="store_true")
    ap.add_argument("--docx-only", action="store_true")
    ap.add_argument("--cover-letter", action="store_true", help="also render cover_letter.md from the same folder")
    ap.add_argument("--from-docx", action="store_true",
                    help="export the PDF from the existing DOCX instead of rebuilding from markdown")
    ap.add_argument("--html-pdf", action="store_true",
                    help="build the PDF from HTML instead of the DOCX (will not match the DOCX)")
    ap.add_argument("--dry-run", action="store_true", help="print the parsed structure and exit")
    ap.add_argument("--tailoring", action="store_true",
                    help="required for newly tailored content; validate career and application readiness first")
    args = ap.parse_args()

    resume_path = os.path.abspath(args.resume)
    folder = os.path.dirname(resume_path)
    out_dir = os.path.abspath(args.out_dir) if args.out_dir else folder
    if args.tailoring:
        from check_readiness import tailoring_errors
        from paths import profile_dir
        try:
            errors = tailoring_errors(profile_dir(args.data_dir, args.profile_dir), folder)
        except (OSError, ValueError, UnicodeError) as exc:
            errors = [str(exc)]
        if errors:
            for error in errors:
                print("BLOCKED: " + error)
            return 3

    cv = parse_markdown_cv(resume_path)
    if args.dry_run:
        print(summary(cv))
        return 0

    profile, pdir = load_profile(args.profile_dir, args.data_dir)
    if profile is None:
        print("ERROR: no profile.yaml at " + pdir + ". Run onboarding first (see SKILL.md).")
        return 1

    os.makedirs(out_dir, exist_ok=True)

    meta = cv.get("meta") or {}
    metadata, metadata_path = read_metadata(folder)
    company = args.company or meta.get("company") or metadata.get("company") or ""
    position = (args.position or meta.get("position") or meta.get("target_title")
                or metadata.get("position") or cv.get("target_title") or "")
    market = pick_market(profile, args.market or meta.get("market") or metadata.get("market"))
    theme = theme_from_profile(profile)
    name = display_name(profile, cv)

    want_pdf = not args.docx_only
    want_docx = not args.pdf_only
    outputs = {}

    cv_base = os.path.splitext(build_filename(theme["filename_pattern"], name, company, position, "CV", ""))[0]
    cl_base = os.path.splitext(build_filename(theme["filename_pattern"], name, company, position, "Cover Letter", ""))[0]

    if args.from_docx:
        docx_path, err = locate_docx(out_dir, cv_base)
        if err:
            print("ERROR: " + err)
            return 1
        res = {"docx": docx_path}
        outputs["cv"] = pdf_from_docx(docx_path, os.path.splitext(docx_path)[0] + ".pdf", res)
        if args.cover_letter:
            cl_docx = os.path.join(out_dir, cl_base + ".docx")
            if os.path.exists(cl_docx):
                outputs["cover_letter"] = pdf_from_docx(cl_docx, os.path.splitext(cl_docx)[0] + ".pdf", {"docx": cl_docx})
        metadata["source_of_truth"] = "docx (hand edited); resume.md may no longer match"
    else:
        import render_docx
        import render_html

        def cv_docx(path):
            render_docx.render_cv_docx(cv, profile, theme, market, path)

        outputs["cv"] = render_one(
            cv_base, out_dir, cv_docx, want_pdf, want_docx,
            html_fn=lambda: render_html.render_cv_html(cv, profile, theme, market),
            use_html_pdf=args.html_pdf)

        if args.cover_letter:
            cl_path = os.path.join(folder, "cover_letter.md")
            if os.path.exists(cl_path):
                with open(cl_path, "r", encoding="utf-8") as f:
                    cl_text = render_html.strip_html_comments(f.read())

                def cl_docx(path):
                    render_docx.render_doc_docx(cl_text, profile, cv, theme, market, path)

                outputs["cover_letter"] = render_one(
                    cl_base, out_dir, cl_docx, want_pdf, want_docx,
                    html_fn=lambda: render_html.render_doc_html(cl_text, profile, cv, theme, market,
                                                                name + " Cover Letter"),
                    use_html_pdf=args.html_pdf)
            else:
                outputs["cover_letter"] = {"error": "cover_letter.md not found in " + folder}
        metadata["source_of_truth"] = "resume.md"

    exit_code = 0
    for doc, res in outputs.items():
        for key in ("docx", "pdf", "pdf_engine", "docx_error", "pdf_error", "pdf_help", "error"):
            if key in res:
                print(doc.upper() + " " + key + ": " + str(res[key]))
        if res.get("docx_error") or res.get("pdf_error"):
            exit_code = max(exit_code, 1)

    pages = None
    limit = market.get("page_limit")
    if outputs.get("cv", {}).get("pdf"):
        pages = render_pdf.count_pages(outputs["cv"]["pdf"])
        print("PAGES: " + str(pages) + " (limit " + str(limit) + ", market " + str(market.get("code")) + ")")
        if pages and limit and pages > int(limit):
            print("OVERFLOW: CV is " + str(pages) + " pages, limit is " + str(limit) +
                  ". Run a brevity pass and re-render.")
            exit_code = 2

    def base(p):
        return os.path.basename(p) if p else None

    metadata.setdefault("company", company)
    metadata.setdefault("position", position)
    metadata["market"] = market.get("code")
    # Basenames, so the folder can move between machines without breaking metadata.
    metadata["outputs"] = {
        "cv_pdf": base(outputs.get("cv", {}).get("pdf")),
        "cv_docx": base(outputs.get("cv", {}).get("docx")),
        "cover_letter_pdf": base(outputs.get("cover_letter", {}).get("pdf")),
        "cover_letter_docx": base(outputs.get("cover_letter", {}).get("docx")),
    }
    metadata["page_count"] = pages
    metadata["last_rendered"] = datetime.now().isoformat(timespec="seconds")
    write_metadata(metadata_path, metadata)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
