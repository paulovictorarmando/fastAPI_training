from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from DTO.UsuarioDTO import UsuarioLogin
from sqlmodel import Session
from Repository.UsuarioRepository import UsuarioRepository
from Config.settings import ENV
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from Config.connection import get_session
from Config.redis import redis_client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 
class AuthService:
	@staticmethod
	def revoke_token(token: str, expires_in: int):
		redis_client.setex(f"blacklist:{token}", timedelta(seconds=expires_in), "revoked")

	@staticmethod
	def is_token_revoked(token: str) -> bool:
		return redis_client.exists(f"blacklist:{token}")

	@staticmethod
	def hash_password(password: str) -> str:
		return pwd_context.hash(password)

	@staticmethod
	def verify_password(plain_password: str, hashed_password: str) -> bool:
		return pwd_context.verify(plain_password, hashed_password)

	@staticmethod
	def create_access_token(data: dict) -> str:
		to_encode = data.copy()
		expire = datetime.now(timezone.utc) + timedelta(minutes=ENV.ACCESS_TOKEN_EXPIRE_MINUTES)
		to_encode.update({"exp": expire})
		encoded_jwt = jwt.encode(to_encode, ENV.SECRET_KEY, algorithm=ENV.ALGORITHM)
		return encoded_jwt

	@staticmethod
	def decode_access_token(token: str) -> dict | None:
		try:
			payload = jwt.decode(token, ENV.SECRET_KEY, algorithms=[ENV.ALGORITHM])
			return payload
		except JWTError:
			return None

	@staticmethod
	def login(session: Session, u_login: UsuarioLogin) -> dict:
		usuario = UsuarioRepository.getByEmail(session, u_login.email)
		if not usuario or not AuthService.verify_password(u_login.senha, usuario.senha):
			raise HTTPException(
					status_code=status.HTTP_401_UNAUTHORIZED,
					detail="Credenciais inválidas"
				)
		token = AuthService.create_access_token({"sub": str(usuario.id)})
		return {"access_token": token, "token_type": "bearer"}

	@staticmethod
	def logout(token: str = Depends(oauth2_scheme)) -> None:
		try:
			payload = AuthService.decode_access_token(token)
			if AuthService.is_token_revoked(token):
				raise HTTPException(
					status_code=status.HTTP_401_UNAUTHORIZED,
					detail="Token inválido ou expirado"
				)
			exp = datetime.fromtimestamp(payload["exp"], timezone.utc)
			expires_in = int((exp - datetime.now(timezone.utc)).total_seconds())
			AuthService.revoke_token(token, expires_in)
			return {"message": "Logout realizado com sucesso!"}
		except Exception:
			raise HTTPException(
					status_code=status.HTTP_401_UNAUTHORIZED,
					detail="Token inválido ou expirado"
				)

	def get_current_user(
		token: str = Depends(oauth2_scheme),
		session: Session = Depends(get_session)
		):
		payload = AuthService.decode_access_token(token)
		if not payload:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token inválido ou expirado",
				headers={"WWW-Authenticate": "Bearer"},
			)

		user_id: str = payload.get("sub")
		if user_id is None:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token inválido",
				headers={"WWW-Authenticate": "Bearer"},
			)
		
		if AuthService.is_token_revoked(token):
			raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token revogado. Faça login novamente.",
			headers={"WWW-Authenticate": "Bearer"},
			)

		user = UsuarioRepository.getById(session, int(user_id))
		if not user:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token inválido",
				headers={"WWW-Authenticate": "Bearer"},
			)

		return user