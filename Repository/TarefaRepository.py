from DTO.TarefaDTO import TarefaCreate, TarefaUpdate
from Models.Tarefa import Tarefa
from sqlmodel import select, Session

class TarefaRepository:
	@staticmethod
	def create(session: Session, tarefa_data: TarefaCreate, user_key: int) -> Tarefa:
		tarefa = Tarefa(**tarefa_data.model_dump(), usuario_id=user_key)
		session.add(tarefa)
		session.commit()
		session.refresh(tarefa)
		return tarefa
	
	@staticmethod
	def getAll(session: Session, user_key: int) -> list[Tarefa]:
		return session.exec(select(Tarefa).where(Tarefa.usuario_id == user_key)).all()
	
	@staticmethod
	def getById(sessin: Session, id: int, user_key: int) -> Tarefa | None:
		return sessin.exec(select(Tarefa).where(
			Tarefa.id == id,
			Tarefa.usuario_id == user_key
		)).first()
	
	@staticmethod
	def getByName(session: Session, nome: str, user_key: int) -> Tarefa | None:
		return session.exec(select(Tarefa).where(
			Tarefa.nome == nome,
			Tarefa.usuario_id == user_key
			)).first()


	@staticmethod
	def delete(session: Session, id: int, user_key: int) -> Tarefa | None:
		tarefa = session.exec(select(Tarefa).where(
			Tarefa.id == id,
			Tarefa.usuario_id == user_key
		)).first()
		if not tarefa or tarefa.usuario_id != user_key:
			return None
		session.delete(tarefa)
		session.commit()
		return tarefa
	
	@staticmethod
	def update(session: Session, id: int, tarefa_update: TarefaUpdate, user_key: int) -> Tarefa | None:
		tarefa = session.exec(select(Tarefa).where(
			Tarefa.id == id, Tarefa.usuario_id == user_key
		))
		if not tarefa or tarefa.usuario_id != user_key:
			return None
		tarefa_para_atualizar = tarefa_update.model_dump(exclude_unset=True)
		for key, value in tarefa_para_atualizar.items():
			setattr(tarefa, key, value)
		session.add(tarefa)
		session.commit()
		session.refresh(tarefa)
		return tarefa