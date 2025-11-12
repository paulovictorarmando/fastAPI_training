from pydantic import BaseModel, Field
from typing import Optional, Annotated

class TarefaCreate(BaseModel):
	nome: Annotated[str, Field(min_length=10, max_length=150)]
	descricao: Annotated[str, Field(min_length=10, max_length=500)]

class TarefaRead(BaseModel):
	id: int 
	nome: str
	descricao: str
	model_config = {"from_attributes": True }

class TarefaUpdate(BaseModel):
	nome: Optional[Annotated[str, Field(min_length=10, max_length=150)]] = None
	descricao: Optional[Annotated[str, Field(min_length=10, max_length=500)]] = None
