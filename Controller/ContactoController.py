from fastapi import Depends, APIRouter, HTTPException, status
from sqlmodel import Session
from DTO.ContactoDTO import ContactoRead, ContactoCreate, ContactoUpdate
from Service.ContactoService import ContactoService
from Service.AuthService import AuthService
from Config.connection import get_session
from Models.Usuario import Usuario

router_contacto = APIRouter(prefix="/contactos", tags=["Contactos"])

@router_contacto.get("/", response_model=list[ContactoRead], status_code=200)
def read_all(
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_current_user)):
	try:
		return ContactoService.read(session,  id=None, user_key=usuario.id)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router_contacto.get("/{id}", response_model=ContactoRead, status_code=200)
def read(
	id: int,
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_current_user)):
	try:
		return ContactoService.read(session,  id=id, user_key=usuario.id)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router_contacto.post("/")
def create(
	contacto: ContactoCreate,
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_current_user)):
	try:
		contacto.usuario_id = usuario.id
		return ContactoService.create(session, contacto, usuario.id)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))
	
@router_contacto.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(
	id: int,
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_current_user)):
	try:
		ContactoService.delete(session, id, user_key=usuario.id)
		return
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router_contacto.patch('/', response_model=list[ContactoRead], status_code=200)
def update(
	contacto: ContactoUpdate,
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_current_user)):
	try:
		return ContactoService.update(session, contacto, user_key=usuario.id)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))