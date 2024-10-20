
from enum import Enum
from typing import Optional # Fiz isso por causa da versão do python


from fastapi import FastAPI

""""
Se você tem uma operação de rota que recebe um parâmetro da rota,
mas que você queira que esses valores possíveis do parâmetro da rota 
sejam predefinidos, você pode usar Enum padrão do Python.
"""
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

#Dados para realização da paginação
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello World" }

@app.get("/users/me")
async def read_user_me():
    return { "user_id": "the_current_user" }

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return { "user_id": user_id }

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

#Exemplo de Query Parameters
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

#Exemplo de Conversão de query parameters
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#Exemplo de múltiplos parâmetros de onsulta
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#Exemplo de parâmetro de consulta obrigatório
""""
quando você quiser fazer com que o parâmetro de consulta seja obrigatório, você pode simplesmente não declarar nenhum valor como padrão.
"""
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item