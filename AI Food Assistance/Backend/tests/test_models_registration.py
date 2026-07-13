from app.database.database import Base
import app.models


def test_user_model_is_registered():
    assert "User" in app.models.__dict__
    assert "users" in Base.metadata.tables
