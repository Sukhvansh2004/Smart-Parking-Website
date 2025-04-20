import pytest
import fastapi
from auth import (
    verify_google_token,
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
)

# Dummy stub for Google's verification
class DummyIDToken:
    @staticmethod
    def verify_oauth2_token(token, request, client_id):
        if token == "valid_token":
            return {"email": "test@example.com"}
        raise Exception("Invalid token")


def test_verify_google_token_valid(monkeypatch):
    import auth
    monkeypatch.setattr(auth.id_token, "verify_oauth2_token", DummyIDToken.verify_oauth2_token)
    result = verify_google_token("valid_token")
    assert result["email"] == "test@example.com"


def test_verify_google_token_invalid(monkeypatch):
    import auth
    monkeypatch.setattr(auth.id_token, "verify_oauth2_token", DummyIDToken.verify_oauth2_token)
    with pytest.raises(fastapi.HTTPException) as excinfo:
        verify_google_token("bad_token")
    assert excinfo.value.status_code == 401


def test_password_hash_and_verify():
    pwd = "secret"
    hashed = get_password_hash(pwd)
    assert verify_password(pwd, hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_encode_decode():
    data = {"sub": "user1"}
    token = create_access_token(data)
    payload = decode_access_token(token)
    assert payload["sub"] == "user1"
    # Test invalid token returns None
    assert decode_access_token("invalid-token") is None
