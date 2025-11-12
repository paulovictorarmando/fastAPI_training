from fastapi import FastAPI
from Config import connection
from contextlib import asynccontextmanager 
from Controller.UsuarioController import router as UsuarioRouter
from Controller.TarefaController import router_tarefa as TarefaRouter
from Controller.ContactoController import router_contacto as ContactoRouter
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
	print("Conexcao criada com sucesso")
	connection.create_db_and_tables()
	yield

app = FastAPI(lifespan=lifespan)

app.include_router(UsuarioRouter)
app.include_router(TarefaRouter)
app.include_router(ContactoRouter)


origins = [
	"http://localhost:5173",  # frontend local (React, Angular, etc)
	"http://127.0.0.1:5173",
	#"https://meu-frontend.com",  # domínio de produção (quando tiver)
]

# 🚀 Middleware de CORS
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,          # permite requisições dessas origens
	allow_credentials=True,         # permite cookies/autenticação
	allow_methods=["*"],            # permite todos os métodos (GET, POST, etc)
	allow_headers=["*"],            # permite todos os headers
)
#print("Rotas registradas no app:")
#for route in app.router.routes:
#    print(route.path)

