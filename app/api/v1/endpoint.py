from fastapi import APIRouter, Depends, HTTPException
from app.services.auth_service import AuthService
from app.schemas.auth_dto import CreateUserDTO, TokenResponseDTO
from app.schemas.login_dto import LoginDTO
from app.core.db_exceptions import EmailAlreadyExists, InvalidCredentialsError
from app.api.dependencies import get_auth_service

router = APIRouter()


@router.post("/create", status_code=201)
async def create_user(
    dto: CreateUserDTO, service: AuthService = Depends(get_auth_service)
):
    try:
        await service.create_new_user(dto)
        return {"mensaje": "Usuario creado con éxito"}
    except EmailAlreadyExists:
        raise HTTPException(status_code=409, detail="Email ya registrado")


@router.post("/login", status_code=200)
async def login_user(dto: LoginDTO, service: AuthService = Depends(get_auth_service)):
    try:
        token = await service.login_user(dto)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Credenciales Inválidas")

    return TokenResponseDTO(access_token=token)
