import os
import secret


def test_secret_loading_from_env():
    assert secret.DATABASE_URL == os.getenv("DATABASE_URL")
    assert secret.SECRET_KEY == os.getenv("SECRET_KEY")
    assert secret.GOOGLE_CLIENT_ID == os.getenv("GOOGLE_CLIENT_ID")
    assert secret.GOOGLE_CLIENT_SECRET == os.getenv("GOOGLE_CLIENT_SECRET")
