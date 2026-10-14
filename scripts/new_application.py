"""Create an application folder from templates/application.

Usage: python new_application.py --company "X" --role "Y" [--market CODE] [--url U] [--location L]
                                 [--date YYYY-MM-DD] [--data-dir D]
Creates <data>/applications/YYYY-MM-DD_company_role/ with job_description.md, roast.md,
cover_letter.md, resume.md (skeleton) and metadata.json. Prints FOLDER: <path>.
"""
import argparse
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from paths import applications_dir, load_profile, TEMPLATES_DIR  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def slug(text):
    text = re.sub(r"[^A-Za-z0-9]+", "_", text.strip().lower())
    return re.sub(r"_+", "_", text).strip("_")[:60]


def fill(text, values):
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--company", required=True)
    ap.add_argument("--role", required=True)
    ap.add_argument("--market")
    ap.add_argument("--url", default="")
    ap.add_argument("--location", default="")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--data-dir")
    args = ap.parse_args()

    profile, _ = load_profile(None, args.data_dir)
    name = ((profile or {}).get("identity") or {}).get("name", "")
    markets = (profile or {}).get("markets") or []
    market = args.market or (markets[0].get("code") if markets else "DEFAULT")
    checkmark = ((profile or {}).get("style") or {}).get("checkmark", "")

    folder = os.path.join(applications_dir(args.data_dir), args.date + "_" + slug(args.company) + "_" + slug(args.role))
    if os.path.exists(folder):
        print("EXISTS: " + folder)
        print("FOLDER: " + folder)
        return 0
    os.makedirs(folder)

    values = {
        "COMPANY": args.company, "ROLE": args.role, "MARKET": market, "URL": args.url,
        "LOCATION": args.location, "DATE": args.date, "FULL_NAME": name, "CHECK": checkmark,
        "EMPLOYMENT_TYPE": "",
    }
    src = os.path.join(TEMPLATES_DIR, "application")
    mapping = {
        "job_description.md": "job_description.md",
        "roast.md": "roast.md",
        "cover_letter.md": "cover_letter.md",
        "resume_skeleton.md": "resume.md",
        "metadata.json": "metadata.json",
        "readiness.yaml": "readiness.yaml",
        "learning.json": "learning.json",
    }
    for tpl, out in mapping.items():
        with open(os.path.join(src, tpl), "r", encoding="utf-8") as f:
            template = f.read()
        if tpl == "metadata.json":
            metadata = json.loads(template)
            text = json.dumps({key: fill(value, values) if isinstance(value, str) else value
                               for key, value in metadata.items()}, indent=2, ensure_ascii=False) + "\n"
        else:
            text = fill(template, values)
        with open(os.path.join(folder, out), "w", encoding="utf-8") as f:
            f.write(text)
        print("WROTE: " + os.path.join(folder, out))
    print("FOLDER: " + folder)
    return 0


if __name__ == "__main__":
    sys.exit(main())
