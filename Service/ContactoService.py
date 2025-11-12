from sqlmodel import Session
from DTO.ContactoDTO import ContactoCreate, ContactoRead, ContactoUpdate
from Repository.ContactoRepository import ContactoRepository

class ContactoService:
	@staticmethod
	def read(session: Session, id : int | None, user_key: int)-> list[ContactoRead] | ContactoRead | None:
		if not id:
			contacts = ContactoRepository.getAll(session, user_key)
			return [ContactoRead.model_validate(c) for c in contacts]
			
		contact = ContactoRepository.getById(id, user_key)
		if not contact:
			raise ValueError("Contacto nao existe!")
		return ContactoRead.model_validate(contact)
			
	@staticmethod
	def create(session: Session, contactocreate: ContactoCreate, user_key: int) -> ContactoRead | None:
		if not ContactoRepository.getByNumber(session, contactocreate.numero, user_key):
			contacto = ContactoRepository.create(session, contactocreate, user_key)
			return ContactoRead.model_validate(contacto)
		raise ValueError("Numero existente!")
	
	@staticmethod
	def delete(session: Session, id: int, user_key: int) -> ContactoRead | None:
		contacto = ContactoRepository.delete(session, id, user_key)
		if not contacto:
			raise ValueError("Contacto nao existe!")
		return ContactoRead.model_validate(contacto)
	
	@staticmethod
	def update(session: Session, contacto_update: ContactoUpdate, user_key: int) -> ContactoRead | None:
		contacto = ContactoRepository.update(session, contacto_update, user_key)
		if not contacto:
			raise ValueError("Contacto nao existe!")
		return ContactoRead.model_validate(contacto)