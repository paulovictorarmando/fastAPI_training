from DTO.ContactoDTO import ContactoCreate, ContactoUpdate
from Models.Contacto import Contacto
from sqlmodel import select, Session

class ContactoRepository:
	@staticmethod
	def create(session: Session, contacto_data: ContactoCreate, user_key: int) -> Contacto:
		contacto = Contacto(**contacto_data.model_dump(), usuario_id=user_key)
		session.add(contacto)
		session.commit()
		session.refresh(contacto)
		return contacto
	
	@staticmethod
	def getAll(session: Session, user_key: int) -> list[Contacto]:
		return session.exec(select(Contacto).where(Contacto.usuario_id == user_key)).all()
	
	@staticmethod
	def getById(sessin: Session, id: int, user_key: int) -> Contacto | None:
		return sessin.exec(select(Contacto).where(
			Contacto.id == id,
			Contacto.usuario_id == user_key
			)).first()
	
	@staticmethod
	def getByName(session: Session, nome: str, user_key: int) -> Contacto | None:
		return session.exec(select(Contacto).where(
			Contacto.nome == nome,
			Contacto.usuario_id == user_key
			)).first()
	
	@staticmethod
	def getByNumber(session: Session, numero: str, user_key: int) -> Contacto | None:
		return session.exec(select(Contacto).where(
			Contacto.numero == numero,
			Contacto.usuario_id == user_key
			)).first()

	@staticmethod
	def delete(session: Session, id: int, user_key: int) -> Contacto | None:
		contacto = session.exec(select(Contacto).where(
			Contacto.id == id,
			Contacto.usuario_id == user_key
		)).first()
		if not contacto or contacto.usuario_id != user_key:
			return None
		session.delete(contacto)
		session.commit()
		return contacto
	
	@staticmethod
	def update(session: Session, id: int, contacto_update: ContactoUpdate, user_key) -> Contacto | None:
		contacto = session.exec(select(Contacto).where(
			Contacto.id == id,
			Contacto.usuario_id == user_key
		)).first()
		if not contacto or contacto.usuario_id != user_key:
			return None
		contacto_para_atualizar = contacto_update.model_dump(exclude_unset=True)
		for key, value in contacto_para_atualizar.items():
			setattr(contacto, key, value)
		session.add(contacto)
		session.commit()
		session.refresh(contacto)
		return contacto