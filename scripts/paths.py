"""Resolve where the user's data lives. Shared by every script.

Resolution order:
  1. JOB_APPLICATIONS_DIR environment variable
  2. ./job-applications (project-local mode)
  3. ~/job-applications (default)

The skill folder itself never holds personal data, so it can be replaced freely.
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKILL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES_DIR = os.path.join(SKILL_DIR, "templates")


def data_dir(explicit=None):
    if explicit:
        return os.path.abspath(os.path.expanduser(explicit))
    env = os.environ.get("JOB_APPLICATIONS_DIR")
    if env:
        return os.path.abspath(os.path.expanduser(env))
    local = os.path.join(os.getcwd(), "job-applications")
    if os.path.isdir(local):
        return local
    return os.path.join(os.path.expanduser("~"), "job-applications")


def profile_dir(data=None, explicit_profile=None):
    if explicit_profile:
        return os.path.abspath(os.path.expanduser(explicit_profile))
    return os.path.join(data_dir(data), "profile")


def applications_dir(data=None):
    return os.path.join(data_dir(data), "applications")


def load_yaml(path):
    """Read complete structured YAML. Never silently drop nested profile information."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    try:
        import yaml  # type: ignore
    except ImportError:
        raise SystemExit("ERROR: PyYAML is required. Use this Python interpreter to install requirements.txt before continuing.")
    try:
        value = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ValueError(str(path) + ": invalid YAML: " + str(exc)) from exc
    if not isinstance(value, dict):
        raise ValueError(str(path) + " must contain a YAML mapping")
    return value


def load_profile(profile=None, data=None):
    """Return (profile_dict_or_None, profile_dir)."""
    pdir = profile_dir(data, profile)
    path = os.path.join(pdir, "profile.yaml")
    if not os.path.exists(path):
        return None, pdir
    return load_yaml(path), pdir


if __name__ == "__main__":
    print("skill_dir:", SKILL_DIR)
    print("data_dir:", data_dir())
    print("profile_dir:", profile_dir())
    prof, _ = load_profile()
    print("profile.yaml:", "found" if prof else "missing")
    if prof:
        print("onboarding_complete:", prof.get("onboarding_complete", False))
        print("schema_version:", prof.get("schema_version"))
