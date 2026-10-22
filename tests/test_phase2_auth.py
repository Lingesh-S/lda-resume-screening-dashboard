import json

import pytest

import auth


@pytest.fixture
def db(tmp_path, monkeypatch):
    path = tmp_path / "users.json"
    monkeypatch.setenv("USER_DB_PATH", str(path))
    return path


def test_hash_round_trip_and_salting():
    first, second = auth.hash_password("s3cret"), auth.hash_password("s3cret")
    assert first != second  # random salt
    assert auth.verify_password("s3cret", first)
    assert not auth.verify_password("wrong", first)


@pytest.mark.parametrize("stored", ["", "plaintext", "md5$1$aa$bb", None])
def test_verify_rejects_malformed_hashes(stored):
    assert not auth.verify_password("s3cret", stored)


def test_create_and_authenticate(db):
    auth.create_user("Asha", "Asha@Example.com", 30, "Female", "pw-123")
    assert auth.authenticate("asha@example.com", "pw-123")["name"] == "Asha"
    assert auth.authenticate("asha@example.com", "nope") is None
    assert auth.authenticate("nobody@example.com", "pw-123") is None


def test_password_never_stored_in_plain_text(db):
    auth.create_user("Asha", "asha@example.com", 30, "Female", "pw-123")
    raw = db.read_text()
    assert "pw-123" not in raw
    assert "password" not in json.loads(raw)["users"][0]


def test_duplicate_email_rejected(db):
    auth.create_user("Asha", "asha@example.com", 30, "Female", "pw-123")
    with pytest.raises(ValueError):
        auth.create_user("Other", "ASHA@example.com", 25, "Other", "pw-456")


def test_missing_fields_rejected(db):
    with pytest.raises(ValueError):
        auth.create_user("", "a@example.com", 30, "Other", "pw")


def test_update_user(db):
    auth.create_user("Asha", "asha@example.com", 30, "Female", "pw-123")
    updated = auth.update_user("asha@example.com", {"score": 42.5})
    assert updated["score"] == 42.5
    assert auth.find_user("asha@example.com")["score"] == 42.5
    assert auth.update_user("missing@example.com", {"score": 1}) is None
