from sqlmodel import Session, select
from Models.Usuario import Usuario
from DTO.UsuarioDTO import UsuarioCreate, UsuarioUpdate

class UsuarioRepository:

	@staticmethod
	def create(session: Session, usuariocreate: UsuarioCreate) -> Usuario:
		
		usuario = Usuario(**usuariocreate.model_dump())
		session.add(usuario)
		session.commit()
		session.refresh(usuario)
		return usuario
	
	@staticmethod
	def getAll(session: Session) -> list[Usuario]:
		return session.exec(select(Usuario)).all()

	@staticmethod
	def getById(session: Session, id: int) -> Usuario | None:
		return session.get(Usuario, id)

	@staticmethod
	def getByEmail(session: Session, email: str) -> Usuario | None:
		usuario = select(Usuario).where(Usuario.email == email)
		return session.exec(usuario).first()
	
	@staticmethod
	def delete(session: Session, id: int) -> Usuario | None:
		usuario = session.get(Usuario, id)
		if not usuario:
			return None
		session.delete(usuario)
		session.commit()
		return usuario

	@staticmethod
	def update(session: Session, id: int, usuario_data: UsuarioUpdate) -> Usuario | None:
		usuario = session.get(Usuario, id)
		if not usuario:
			return None
		dados_para_atualizar = usuario_data.model_dump(exclude_unset=True)
		for key, value in dados_para_atualizar.items():
			setattr(usuario, key, value)
		session.add(usuario)
		session.commit()
		session.refresh(usuario)
		return usuario