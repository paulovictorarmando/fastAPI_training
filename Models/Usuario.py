from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .Tarefa import Tarefa
from .Contacto import Contacto

class Usuario(SQLModel, table=True):
	id: Optional[int] = Field(default = None, primary_key = True)
	nome: str = Field(nullable=False, max_length = 150)
	email: str = Field(nullable=False, unique=True)
	senha: str = Field(nullable=False)

	contactos: List["Contacto"] = Relationship(back_populates="usuario")
	tarefas: List["Tarefa"] = Relationship(back_populates="usuario")