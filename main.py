from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.todo_routes import todo_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get('/ping')
def ping():
   return 'pong'

app.include_router(todo_routes)