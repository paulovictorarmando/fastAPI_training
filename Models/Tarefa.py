from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Tarefa(SQLModel, table=True):
	id: Optional[int] = Field(default = None, primary_key = True)
	nome: str = Field(nullable=False, max_length = 150, unique=True)
	descricao: str = Field(nullable=False, max_length = 500)
	usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

	usuario: Optional["Usuario"] = Relationship(back_populates="tarefas")