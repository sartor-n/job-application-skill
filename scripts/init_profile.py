"""Scaffold the data directory: profile/ from templates, plus applications/ and profile/knowledge/.

Usage: python init_profile.py [--data-dir D] [--force]
Refuses to overwrite existing profile files unless --force (which backs them up first).
"""
import argparse
import os
import shutil
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from paths import data_dir, TEMPLATES_DIR  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    root = data_dir(args.data_dir)
    pdir = os.path.join(root, "profile")
    src = os.path.join(TEMPLATES_DIR, "profile")
    existing = [n for n in os.listdir(src) if os.path.exists(os.path.join(pdir, n))] if os.path.isdir(pdir) else []
    if existing and not args.force:
        print("EXISTS: profile files already present in " + pdir + ": " + ", ".join(existing))
        print("Nothing written. Use --force to back up and replace them, or run 'profile edit' instead.")
        return 3
    if existing and args.force:
        backup = os.path.join(root, "profile_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        shutil.copytree(pdir, backup)
        print("BACKUP: " + backup)

    for sub in (pdir, os.path.join(pdir, "knowledge"), os.path.join(root, "applications")):
        os.makedirs(sub, exist_ok=True)
    for name in os.listdir(src):
        shutil.copy2(os.path.join(src, name), os.path.join(pdir, name))
        print("WROTE: " + os.path.join(pdir, name))
    readme = os.path.join(pdir, "knowledge", "README.md")
    if not os.path.exists(readme):
        with open(readme, "w", encoding="utf-8") as f:
            f.write("# Knowledge\n\nExtra facts about your experience that are not in master_cv.md, one file per topic. "
                    "The assistant saves confirmed reusable evidence here with its intended scope. "
                    "See ../preferences.md for active rules and superseding corrections; application-only facts stay local.\n")
    print("DATA_DIR: " + root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
