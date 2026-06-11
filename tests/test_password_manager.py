"""Test suite for the Password Manager core behavior.

Covers password generation/validation, the Fernet encrypt/decrypt round trip
(including the retrieve bug that used to double-decode), wrong-key handling,
and the JSON save/get/delete flow against a temporary database directory.

Run from the repository root:

    python -m pytest
"""
import base64
import os
import sys

import pytest
from cryptography.fernet import InvalidToken

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from model.password import Password
from views.password_views import FernetHasher


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    """Point the model's DB_DIR at an isolated tmp directory."""
    db_dir = tmp_path / "db"
    monkeypatch.setattr(Password, "DB_DIR", db_dir)
    return db_dir


# --- Password generation / validation -------------------------------------

def test_generate_password_meets_complexity():
    pwd = Password.generate_password(length=16)
    assert len(pwd) == 16
    assert Password.validate_password(pwd)


def test_generate_password_rejects_short_length():
    with pytest.raises(ValueError):
        Password.generate_password(length=4)


@pytest.mark.parametrize(
    "candidate,expected",
    [
        ("Abcd1234!", True),
        ("short1!A", True),
        ("alllowercase1!", False),   # no uppercase
        ("ALLUPPERCASE1!", False),   # no lowercase
        ("NoDigits!!", False),       # no digit
        ("NoSpecial123", False),     # no special char
        ("Ab1!", False),             # too short
    ],
)
def test_validate_password(candidate, expected):
    assert Password.validate_password(candidate) is expected


# --- Encryption round trip -------------------------------------------------

def test_create_key_is_urlsafe():
    key, _ = FernetHasher.create_key(archive=False)
    # URL-safe base64 never contains '+' or '/'.
    assert b"+" not in key and b"/" not in key
    # Must still decode to a valid 32-byte Fernet key.
    assert len(base64.urlsafe_b64decode(key)) == 32


def test_encrypt_decrypt_round_trip():
    key, _ = FernetHasher.create_key(archive=False)
    fernet = FernetHasher(key)
    token = fernet.encrypt("Minha senha").decode("utf-8")
    # decrypt returns a str directly (no second .decode needed).
    assert fernet.decrypt(token.encode()) == "Minha senha"


def test_decrypt_with_wrong_key_raises():
    key1, _ = FernetHasher.create_key(archive=False)
    key2, _ = FernetHasher.create_key(archive=False)
    token = FernetHasher(key1).encrypt("secret").decode("utf-8")
    with pytest.raises(InvalidToken):
        FernetHasher(key2).decrypt(token.encode())


# --- Save / get / delete ---------------------------------------------------

def test_save_and_get(tmp_db):
    Password(domain="github.com", password="enc", notes="n").save()
    rows = Password.get()
    assert len(rows) == 1
    assert rows[0]["domain"] == "github.com"


def test_save_updates_existing_domain(tmp_db):
    Password(domain="github.com", password="enc1").save()
    Password(domain="github.com", password="enc2").save()
    rows = Password.get()
    assert len(rows) == 1
    assert rows[0]["password"] == "enc2"


def test_delete_is_case_insensitive(tmp_db):
    Password(domain="GitHub.com", password="enc").save()
    assert Password.delete("github.com") is True
    assert Password.get() == []


def test_delete_missing_returns_false(tmp_db):
    assert Password.delete("nope.com") is False


def test_list_domains(tmp_db):
    Password(domain="a.com", password="e1").save()
    Password(domain="b.com", password="e2").save()
    assert sorted(Password.list_domains()) == ["a.com", "b.com"]
