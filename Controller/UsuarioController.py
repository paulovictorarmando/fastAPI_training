from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from Config.connection import get_session
from DTO.UsuarioDTO import UsuarioCreate, UsuarioRead, UsuarioLogin
from Service.UsuarioService import UsuarioService
from Service.AuthService import AuthService
from Models.Usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/create", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def create_user(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    try:
        return UsuarioService.create(session, usuario)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int,
    session: Session = Depends(get_session),
	current_user: Usuario = Depends(AuthService.get_current_user)):
	try:
		UsuarioService.delete(session, id)
		return 
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(usuario: UsuarioLogin, session: Session = Depends(get_session)):
    try:
        return AuthService.login(session, usuario)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_BAD_REQUEST, detail=str(e))
    
@router.post("/logout")
def logout_endpoint(
	message = Depends(AuthService.logout)):
		return message