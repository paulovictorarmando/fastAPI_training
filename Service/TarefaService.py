from DTO.TarefaDTO import TarefaCreate, TarefaUpdate, TarefaRead
from sqlmodel import Session
from Repository.TarefaRepository import TarefaRepository

class TarefaService:
	@staticmethod
	def read(session: Session, id : int | None, user_key: int)-> list[TarefaRead] | TarefaRead | None:
		if not id:
			tarefas = TarefaRepository.getAll(session, user_key)
			return [TarefaRead.model_validate(tarefa) for tarefa in tarefas]
		tarefa = TarefaRepository.getById(id, user_key)
		if not tarefa:
			raise ValueError("Tarefa nao existe!")
		return TarefaRead.model_validate(tarefa)
			
	@staticmethod
	def create(session: Session, tarefacreate: TarefaCreate, user_key: int) -> TarefaRead | None:
		if not TarefaRepository.getByName(session, tarefacreate.nome, user_key):
			tarefa = TarefaRepository.create(session, tarefacreate, user_key)
			return TarefaRead.model_validate(tarefa)
		raise ValueError("Tarefa existente!")
	
	@staticmethod
	def delete(session: Session, id: int, user_key: int) -> TarefaRead | None:
		tarefa = TarefaRepository.delete(session, id, user_key)
		if not tarefa:
			raise ValueError("Tarefa nao existe!")
		return TarefaRead.model_validate(tarefa)
	
	@staticmethod
	def update(session: Session, tarefa_update: TarefaUpdate, user_key: int) -> TarefaRead | None:
		tarefa = TarefaRepository.update(session, tarefa_update, user_key)
		if not tarefa:
			raise ValueError("Tarefa nao existe!")
		return TarefaRead.model_validate(tarefa)
