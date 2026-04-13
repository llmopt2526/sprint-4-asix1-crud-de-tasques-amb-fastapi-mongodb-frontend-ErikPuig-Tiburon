import os
from typing import Optional, List

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from bson import ObjectId
import asyncio
from pymongo import AsyncMongoClient
from pymongo import ReturnDocument

# ------------------------------------------------------------------------ #
#                         Inicialització de l'aplicació                    #
# ------------------------------------------------------------------------ #
# Creació de la instància FastAPI amb informació bàsica de l'API
app = FastAPI(
    title="Gestor de Tasques",
    summary="Aplicacio per a controla un Gestor de Tasques via FastAPI ",
)

# ------------------------------------------------------------------------ #
#                   Configuració de la connexió amb MongoDB                #
# ------------------------------------------------------------------------ #
# Creem el client de MongoDB utilitzant la URL de connexió emmagatzemada
# a les variables d'entorn. Això evita incloure credencials dins del codi.
client = AsyncMongoClient(os.environ["MONGODB_URL"])

# Selecció de la base de dades i de la col·lecció
db = client.gestor
task_collection = db.get_collection("tasques")


# Els documents de MongoDB tenen `_id` de tipus ObjectId.
# Aquí definim PyObjectId com un string serialitzable per JSON,
# que serà utilitzat als models Pydantic.
PyObjectId = Annotated[str, BeforeValidator(str)]

# ------------------------------------------------------------------------ #
#                            Definició dels models                         #
# ------------------------------------------------------------------------ #
class TascaModel(BaseModel):
    """
    Model que representa un estudiant.
    Conté tots els camps obligatoris i opcional `_id`.
    """
    # Clau primària de l'estudiant.
    # MongoDB utilitza `_id`, però l'API exposa aquest camp com `id`.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    # Camps obligatoris de l'estudiant
    class TascaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    titol: str = Field(...)
    descripcio: str = Field(...)
    estat: str = Field(default="pendent")
    prioritat: str = Field(default="alta")
    categoria: str = Field(...)
    persona_assignada: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "titol": "Fer pràctica FastAPI",
                "descripcio": "Implementar CRUD amb MongoDB",
                "estat": "pendent",
                "prioritat": "alta",
                "categoria": "estudis",
                "persona_assignada": "Paco"
            }
        },
    )
# ------------------------------------------------------------------------ #
#                       Models d'actualització                             #
# ------------------------------------------------------------------------ #

class UpdateTascaModel(BaseModel):
    """
    Camps opcionals per actualitzar una tasca.
    Només s'actualitzen els camps enviats.
    """

    titol: Optional[str] = None
    descripcio: Optional[str] = None
    estat: Optional[str] = None
    prioritat: Optional[str] = None
    categoria: Optional[str] = None
    persona_assignada: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "titol": "Fer pràctica FastAPI",
                "descripcio": "CRUD complet",
                "estat": "feta",
                "prioritat": "alta",
                "categoria": "estudis",
                "persona_assignada": "Paco"
            }
        },
    )


# ------------------------------------------------------------------------ #
#                       Contenidor de col·lecció                           #
# ------------------------------------------------------------------------ #

class TascaCollection(BaseModel):
    """
    Contenidor de llista de tasques (evita retornar arrays directes).
    """
    tasques: List[TascaModel]


# ------------------------------------------------------------------------ #
#                           CREATE                                         #
# ------------------------------------------------------------------------ #

@app.post(
    "/tasques/",
    response_description="Afegir nova tasca",
    response_model=TascaModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_tasca(tasca: TascaModel = Body(...)):
    new_tasca = tasca.model_dump(by_alias=True, exclude=["id"])
    result = await task_collection.insert_one(new_tasca)
    new_tasca["_id"] = result.inserted_id
    return new_tasca


# ------------------------------------------------------------------------ #
#                           READ ALL                                       #
# ------------------------------------------------------------------------ #

@app.get(
    "/tasques/",
    response_description="Llistar totes les tasques",
    response_model=TascaCollection,
    response_model_by_alias=False,
)
async def list_tasques():
    return TascaCollection(
        tasques=await task_collection.find().to_list(1000)
    )


# ------------------------------------------------------------------------ #
#                           READ ONE                                       #
# ------------------------------------------------------------------------ #

@app.get(
    "/tasques/{id}",
    response_description="Obtenir una tasca",
    response_model=TascaModel,
    response_model_by_alias=False,
)
async def show_tasca(id: str):
    if (tasca := await task_collection.find_one({"_id": ObjectId(id)})) is not None:
        return tasca

    raise HTTPException(status_code=404, detail=f"Tasca {id} no trobada")


# ------------------------------------------------------------------------ #
#                           UPDATE                                         #
# ------------------------------------------------------------------------ #

@app.put(
    "/tasques/{id}",
    response_description="Actualitzar una tasca",
    response_model=TascaModel,
    response_model_by_alias=False,
)
async def update_tasca(id: str, tasca: UpdateTascaModel = Body(...)):

    tasca = {
        k: v for k, v in tasca.model_dump(by_alias=True).items() if v is not None
    }

    if len(tasca) >= 1:
        update_result = await task_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": tasca},
            return_document=ReturnDocument.AFTER,
        )

        if update_result is not None:
            return update_result

        raise HTTPException(status_code=404, detail=f"Tasca {id} no trobada")

    # Si no s'envia res, retorna la tasca igualment
    if (existing := await task_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing

    raise HTTPException(status_code=404, detail=f"Tasca {id} no trobada")


# ------------------------------------------------------------------------ #
#                           DELETE                                         #
# ------------------------------------------------------------------------ #

@app.delete("/tasques/{id}", response_description="Eliminar una tasca")
async def delete_tasca(id: str):
    delete_result = await task_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Tasca {id} no trobada")
