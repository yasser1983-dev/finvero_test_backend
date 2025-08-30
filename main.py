from fastapi import FastAPI

# Crea una instancia de FastAPI
app = FastAPI()

# Define una ruta GET para la URL raíz ("/")
@app.get("/")
def read_root():
    return {"Hello": "World"}