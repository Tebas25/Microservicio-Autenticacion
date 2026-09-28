from fastapi import Depends
from app.db.session import get_database
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService


def get_auth_service(db=Depends(get_database)) -> AuthService:
    repo = AuthRepository(db)
    return AuthService(repo)
