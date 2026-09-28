from datetime import datetime
import uuid
from sqlalchemy import String, Boolean, DateTime, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class UsuarioAdmin(Base):
    __tablename__ = "usuarios_admin"

    id_usuario: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    nombre_completo: Mapped[str] = mapped_column(String)
    estado: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )
