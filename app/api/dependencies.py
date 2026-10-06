from fastapi import Depends
from app.db.session import get_database
from app.core.config import get_jwt_setting, Settings
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService


def get_auth_service(
    db=Depends(get_database),
    settings: Settings = Depends(get_jwt_setting),
) -> AuthService:
    repo = AuthRepository(db)
    return AuthService(repo, settings)
