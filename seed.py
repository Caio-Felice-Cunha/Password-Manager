"""Seed the local database with demo entries.

The real database (db/Password.json) and key files are intentionally NOT
committed (a password manager must never ship key material). This script
recreates a small demo dataset on a fresh checkout so you can try the
retrieve, list, delete, and backup flows immediately.

Run from the repository root:

    python seed.py

It prints the demo encryption key. Use that key when the menu asks for one
(menu option 2, "Retrieve password"). The key is generated fresh each run and
is never written into version control.
"""
import sys
import os

sys.path.append(os.path.abspath(os.curdir))

from model.password import Password
from views.password_views import FernetHasher

DEMO_ENTRIES = [
    {"domain": "github.com", "password": "Gh!demoPass1", "notes": "demo account"},
    {"domain": "gmail.com", "password": "Mail#demo42", "notes": ""},
    {"domain": "youtube.com", "password": "Yt$watch2026", "notes": "shared family login"},
]


def seed():
    key, _ = FernetHasher.create_key(archive=False)
    fernet = FernetHasher(key)

    # Start from a clean table so reruns stay deterministic.
    table_path = Password.DB_DIR / "Password.json"
    if table_path.exists():
        table_path.unlink()

    for item in DEMO_ENTRIES:
        encrypted = fernet.encrypt(item["password"]).decode("utf-8")
        entry = Password(domain=item["domain"], password=encrypted, notes=item["notes"])
        entry.save()

    print("Seeded {} demo entries into {}".format(len(DEMO_ENTRIES), table_path))
    print("Demo encryption key (use it for option 2, Retrieve password):")
    print(key.decode("utf-8"))


if __name__ == "__main__":
    seed()
