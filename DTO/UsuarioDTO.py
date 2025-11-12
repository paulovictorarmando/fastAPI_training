from pydantic import EmailStr, BaseModel, Field
from typing import Optional, Annotated

class UsuarioCreate(BaseModel):
	nome: Annotated[str, Field(min_length=10, max_length=150)]
	email: EmailStr
	senha: Annotated[str, Field(min_length=6, max_length=100)] = None


class UsuarioRead(BaseModel):
	id: int
	nome: str
	email: Optional[str] = None
	model_config = {"from_attributes": True }

class UsuarioUpdate(BaseModel):
	nome: Optional[Annotated[str, Field(min_length=10, max_length=150)]] = None
	email: Optional[EmailStr] = None
	senha: Optional[Annotated[str, Field(min_length=6, max_length=100)]] = None

class UsuarioLogin(BaseModel):
	email: EmailStr
	senha: str