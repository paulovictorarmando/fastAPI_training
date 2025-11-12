from fastapi import Depends, APIRouter, HTTPException, status
from sqlmodel import Session
from DTO.TarefaDTO import TarefaRead, TarefaCreate, TarefaUpdate
from Service.TarefaService import TarefaService
from Service.AuthService import AuthService
from Config.connection import get_session
from Models.Usuario import Usuario

router_tarefa = APIRouter(prefix="/tarefas", tags=["Tarefas"])

@router_tarefa.get("/", response_model=list[TarefaRead], status_code=200)
def read_all(
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_current_user)):
	try:
		data = TarefaService.read(session,  id=None, user_key=usuario.id)
		print(f'\n\n\n\nDados do retorno: {data}\n\n\n\n')
		return data
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router_tarefa.get("/{id}", response_model=TarefaRead, status_code=200)
def read(
	id: int,
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_current_user)):
	try:
		return TarefaService.read(session,  id=id, user_key=usuario.id)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router_tarefa.post("/")
def create(
	tarefa: TarefaCreate,
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_current_user)):
	try:
		return TarefaService.create(session, tarefa, usuario.id)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))
	
@router_tarefa.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(
	id: int,
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_current_user)):
	try:
		TarefaService.delete(session, id, user_key=usuario.id)
		return
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router_tarefa.patch('/', response_model=list[TarefaRead], status_code=200)
def update(
	tarefa: TarefaUpdate,
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_current_user)):
	try:
		return TarefaService.update(session, tarefa, user_key=usuario.id)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))