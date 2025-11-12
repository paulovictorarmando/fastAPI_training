from pydantic import EmailStr, BaseModel, Field, field_validator
from typing import Optional, Annotated
import re

class ContactoCreate(BaseModel):
	nome: Annotated[str, Field(min_length=10, max_length=150)]
	email: Optional[EmailStr] = None
	numero: Annotated[str, Field(min_length=9, max_length=13)]
	@field_validator("numero")
	@classmethod
	def validar_numero(cls, v):
		padrao = r"^\+?\d{9,13}$"
		if not re.fullmatch(padrao, v):
			raise ValueError("O número deve conter apenas dígitos.")
		return v

class ContactoRead(BaseModel):
	id: int
	nome: str
	email: Optional[str] = None
	numero: str
	model_config = {"from_attributes": True }

class ContactoUpdate(BaseModel):
	nome: Optional[Annotated[str, Field(min_length=10, max_length=150)]] = None
	email: Optional[EmailStr] = None
	numero: Optional[Annotated[str, Field(min_length=9, max_length=13)]] = None
	@field_validator("numero")
	@classmethod
	def validar_numero(cls, v):
		padrao = r"^\+?\d{9,13}$"
		if not re.fullmatch(padrao, v):
			raise ValueError("O número deve conter apenas dígitos.")
		return v