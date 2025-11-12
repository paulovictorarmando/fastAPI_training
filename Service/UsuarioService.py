from Repository.UsuarioRepository import UsuarioRepository
from DTO.UsuarioDTO import UsuarioCreate, UsuarioRead, UsuarioLogin
from sqlmodel import Session
from Service.AuthService import AuthService

class UsuarioService:
	@staticmethod
	def create(session: Session, usuariocreate: UsuarioCreate) -> UsuarioRead | None:
		usuario_existente = UsuarioRepository.getByEmail(session, usuariocreate.email)
		if usuario_existente:
			raise ValueError("Conta já existente!")
		usuariocreate.senha = AuthService.hash_password(usuariocreate.senha)
		usuario = UsuarioRepository.create(session, usuariocreate)
		return UsuarioRead.model_validate(usuario)
	
	@staticmethod
	def delete(session: Session, usser_key: int):
		usuario = UsuarioRepository.getById(session, usser_key)
		if not usuario:
			raise ValueError("conta inexistente!")
		UsuarioRepository.delete(session, usser_key)
		return UsuarioRead.model_validate(usuario)
