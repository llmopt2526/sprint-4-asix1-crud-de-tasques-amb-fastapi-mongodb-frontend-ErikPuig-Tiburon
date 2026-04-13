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
    prioritat: str = Field(...)
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
