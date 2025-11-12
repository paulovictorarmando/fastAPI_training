from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Contacto(SQLModel, table=True):
	id: Optional[int] = Field(default = None, primary_key = True)
	nome: str = Field(nullable=False, max_length = 150)
	email: str = Field(nullable=True, unique=True)
	numero: str = Field(nullable=False, unique=True, max_length= 13)
	usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

	usuario: Optional["Usuario"] = Relationship(back_populates="contactos")