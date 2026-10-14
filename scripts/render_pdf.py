"""PDF export.

The DOCX is the single definition of the document's layout. The PDF is exported from it, so
what you see in Word is what you submit, and hand edits to the DOCX flow into the PDF.

Engines, in order (override with CV_PDF_ENGINE=word|libreoffice|browser):
  1. Microsoft Word through COM (Windows, needs Word and pywin32). The reference renderer for
     .docx, so a document edited in Word exports exactly as it looked.
  2. LibreOffice headless. Cross-platform, uses an isolated profile so it works even when
     LibreOffice is already open.
  3. Headless Chromium from HTML. Opt-in escape hatch only. It does not read the DOCX, so its
     output will not match the DOCX exactly. Used only when asked for with --html-pdf.
"""
import os
import re
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SOFFICE_PATHS = [
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/usr/bin/soffice",
    "/usr/bin/libreoffice",
]
PATH_NAMES = ["msedge", "microsoft-edge", "google-chrome", "google-chrome-stable", "chrome",
              "chromium", "chromium-browser", "brave", "brave-browser"]
WINDOWS_BROWSERS = [
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
]
MAC_BROWSERS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]

WD_EXPORT_FORMAT_PDF = 17


def find_soffice():
    found = shutil.which("soffice") or shutil.which("libreoffice")
    if found:
        return found
    for path in SOFFICE_PATHS:
        if os.path.exists(path):
            return path
    return None


def have_word():
    """True when Word plus pywin32 are usable on this machine."""
    if os.name != "nt":
        return False
    try:
        import win32com.client  # noqa: F401
    except ImportError:
        return False
    try:
        import winreg
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Word.Application")
        return True
    except OSError:
        return False


def find_browser():
    env = os.environ.get("CV_BROWSER")
    if env:
        if os.path.exists(env) or shutil.which(env):
            return env
        print("WARNING: CV_BROWSER is set to '" + env + "' but it does not exist. Falling back to detection.")
    for name in PATH_NAMES:
        found = shutil.which(name)
        if found:
            return found
    for path in WINDOWS_BROWSERS + MAC_BROWSERS:
        if os.path.exists(path):
            return path
    return None


def word_docx_to_pdf(docx_path, pdf_path):
    """Export through Word itself. Most faithful for a document edited in Word."""
    try:
        import pythoncom  # type: ignore
        import win32com.client  # type: ignore
    except ImportError:
        return False, "pywin32 not installed (pip install pywin32)"
    docx_path, pdf_path = os.path.abspath(docx_path), os.path.abspath(pdf_path)
    pythoncom.CoInitialize()
    word = doc = None
    try:
        # DispatchEx starts a private instance, so an open Word session is left alone.
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        doc = word.Documents.Open(docx_path, ReadOnly=True, AddToRecentFiles=False)
        doc.ExportAsFixedFormat(OutputFileName=pdf_path, ExportFormat=WD_EXPORT_FORMAT_PDF)
    except Exception as e:  # noqa: BLE001
        return False, "Word: " + str(e).strip()[-300:]
    finally:
        try:
            if doc is not None:
                doc.Close(False)
        except Exception:  # noqa: BLE001
            pass
        try:
            if word is not None:
                word.Quit()
        except Exception:  # noqa: BLE001
            pass
        pythoncom.CoUninitialize()
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        return True, "Microsoft Word"
    return False, "Word produced no PDF"


def soffice_docx_to_pdf(docx_path, pdf_path, timeout=180):
    soffice = find_soffice()
    if not soffice:
        return False, "LibreOffice (soffice) not found"
    docx_path, pdf_path = os.path.abspath(docx_path), os.path.abspath(pdf_path)
    out_dir = os.path.dirname(pdf_path)
    # A private user profile so the conversion works even when LibreOffice is already running.
    profile = os.path.join(os.path.expanduser("~"), ".cache", "job-application-soffice")
    os.makedirs(profile, exist_ok=True)
    profile_url = "file:///" + profile.replace("\\", "/").lstrip("/")
    cmd = [soffice, "-env:UserInstallation=" + profile_url, "--headless", "--norestore",
           "--convert-to", "pdf", "--outdir", out_dir, docx_path]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, "LibreOffice timed out after " + str(timeout) + "s"
    produced = os.path.join(out_dir, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf")
    if os.path.exists(produced):
        if os.path.abspath(produced) != pdf_path:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            os.replace(produced, pdf_path)
        return True, "LibreOffice"
    return False, "LibreOffice: " + (res.stderr or res.stdout or "produced no PDF").strip()[-300:]


def docx_to_pdf(docx_path, pdf_path):
    """Export the DOCX to PDF. Returns (ok, engine_or_error)."""
    if not os.path.exists(docx_path):
        return False, "DOCX not found: " + docx_path
    if os.path.exists(pdf_path):
        try:
            os.remove(pdf_path)
        except OSError as e:
            return False, "cannot replace the PDF, it may be open in a viewer: " + str(e)

    forced = (os.environ.get("CV_PDF_ENGINE") or "").strip().lower()
    engines = []
    if forced == "word":
        engines = [word_docx_to_pdf]
    elif forced in ("libreoffice", "soffice"):
        engines = [soffice_docx_to_pdf]
    else:
        if have_word():
            engines.append(word_docx_to_pdf)
        engines.append(soffice_docx_to_pdf)

    notes = []
    for fn in engines:
        ok, note = fn(docx_path, pdf_path)
        if ok:
            return True, note
        notes.append(note)
    if not notes:
        notes.append("no converter selected")
    return False, " | ".join(notes)


def html_to_pdf(html_path, pdf_path, browser=None, timeout=90):
    """Opt-in escape hatch. Does not read the DOCX, so the layout will differ from it."""
    browser = browser or find_browser()
    if not browser:
        return False, "no Chromium browser found (set CV_BROWSER or install Edge, Chrome, Chromium or Brave)"
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    cmd = [
        browser, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
        "--disable-extensions", "--no-pdf-header-footer", "--virtual-time-budget=4000",
        "--print-to-pdf=" + os.path.abspath(pdf_path),
        "file:///" + os.path.abspath(html_path).replace("\\", "/"),
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, "browser timed out after " + str(timeout) + "s"
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        return True, browser
    cmd[1] = "--headless"  # older builds
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        return True, browser
    return False, (res.stderr or res.stdout or "browser produced no PDF").strip()[-300:]


def missing_converter_help():
    return ("No DOCX to PDF converter found. Install LibreOffice (free, libreoffice.org) or "
            "Microsoft Word plus pywin32 (pip install pywin32). The DOCX was still written, so "
            "you can export a PDF from Word yourself. To use the browser instead, which produces "
            "a PDF that will not match the DOCX exactly, pass --html-pdf.")


def count_pages(pdf_path):
    try:
        from pypdf import PdfReader  # type: ignore
        return len(PdfReader(pdf_path).pages)
    except Exception:  # noqa: BLE001
        pass
    try:
        with open(pdf_path, "rb") as f:
            data = f.read()
        n = len(re.findall(rb"/Type\s*/Page[^s]", data))
        return n or None
    except Exception:  # noqa: BLE001
        return None


if __name__ == "__main__":
    print("word:", "available" if have_word() else "not available")
    print("soffice:", find_soffice() or "none")
    print("browser (escape hatch):", find_browser() or "none")
    forced = os.environ.get("CV_PDF_ENGINE")
    if forced:
        print("CV_PDF_ENGINE:", forced)
