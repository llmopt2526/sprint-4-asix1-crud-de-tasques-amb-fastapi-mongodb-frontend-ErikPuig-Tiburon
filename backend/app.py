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

# Ací es on creem la app de FastAPI, que al final es la base de tot el xiringuito
app = FastAPI(
    title="Gestor de Tasques",
    summary="Aplicacio per a controla un Gestor de Tasques via FastAPI ",
)
from fastapi.middleware.cors import CORSMiddleware
# Aixo es pa que el navegador no toque massa els collons en el frontend
# Basicament deixem passar peticions des de qualsevol puesto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------------ #
#                   Configuració de la connexió amb MongoDB                #
# ------------------------------------------------------------------------ #

# Ací me conecto a MongoDB usant la variable d'entorn MONGODB_URL
# Aixina no fiquem la URL ni contrasenyes directament al codi
client = AsyncMongoClient(os.environ["MONGODB_URL"])

# Seleccionem la base de dades i la col·lecció que gastarem
db = client.gestor
task_collection = db.get_collection("tasques")

# MongoDB treballa en _id amb ObjectId, pero nosaltres volem tractarlo com si fora string
# Aixina després FastAPI ho pòt enviar millor en JSON
PyObjectId = Annotated[str, BeforeValidator(str)]


# ------------------------------------------------------------------------ #
#                            Definició dels models                         #
# ------------------------------------------------------------------------ #

# Este model es el bo de les tasques, en tots els camps que demana l'enunciat
class TascaModel(BaseModel):
    # La id de MongoDB, pero exposada de forma mes usable
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    # Ací van els camps de la tasca
    titol: str = Field(...)
    descripcio: str = Field(...)
    estat: str = Field(default="pendent")
    prioritat: str = Field(default="alta")
    categoria: str = Field(...)
    persona_assignada: str = Field(...)

    # Config extra pa que Pydantic no plore i de pas fique un example bonico al /docs
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

# Este model es pa quan vols editar una tasca i no cal enviar-ho tot
# Solament envies els camps que vols canviar
class UpdateTascaModel(BaseModel):
    titol: Optional[str] = None
    descripcio: Optional[str] = None
    estat: Optional[str] = None
    prioritat: Optional[str] = None
    categoria: Optional[str] = None
    persona_assignada: Optional[str] = None

    # Mateixa idea que abans, pero pa updates
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

# Aixo es pa retornar les tasques dins d'un objecte i no com un array pelat
# Queda mes net i es la forma que has gastat al frontend
class TascaCollection(BaseModel):
    tasques: List[TascaModel]


# ------------------------------------------------------------------------ #
#                           CREATE                                         #
# ------------------------------------------------------------------------ #

# Ací creem una tasca nova
@app.post(
    "/tasques/",
    response_description="Afegir nova tasca",
    response_model=TascaModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_tasca(tasca: TascaModel = Body(...)):
    # Convertim la tasca a diccionari i li llevem la id perque Mongo la crea sola
    new_tasca = tasca.model_dump(by_alias=True, exclude=["id"])

    # La guardem en MongoDB
    result = await task_collection.insert_one(new_tasca)

    # Li tornem a ficar la _id que ha generat Mongo pa retornar-la
    new_tasca["_id"] = result.inserted_id
    return new_tasca


# ------------------------------------------------------------------------ #
#                           READ ALL                                       #
# ------------------------------------------------------------------------ #

# Ací tornem totes les tasques de la coleccio
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

# Ací busquem una tasca concreta per la seua id
@app.get(
    "/tasques/{id}",
    response_description="Obtenir una tasca",
    response_model=TascaModel,
    response_model_by_alias=False,
)
async def show_tasca(id: str):
    # Si la trobem, la retornem
    if (tasca := await task_collection.find_one({"_id": ObjectId(id)})) is not None:
        return tasca

    # Si no la trobem, pam, error 404
    raise HTTPException(status_code=404, detail=f"Tasca {id} no trobada")


# ------------------------------------------------------------------------ #
#                           UPDATE                                         #
# ------------------------------------------------------------------------ #

# Ací actualitzem una tasca ja existent
@app.put(
    "/tasques/{id}",
    response_description="Actualitzar una tasca",
    response_model=TascaModel,
    response_model_by_alias=False,
)
async def update_tasca(id: str, tasca: UpdateTascaModel = Body(...)):

    # Ací filtre els camps per no enviar els que venen en None
    tasca = {
        k: v for k, v in tasca.model_dump(by_alias=True).items() if v is not None
    }

    # Si hi ha algo pa actualitzar, fem el update
    if len(tasca) >= 1:
        update_result = await task_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": tasca},
            return_document=ReturnDocument.AFTER,
        )

        # Si ha anat be, tornem la tasca actualitzada
        if update_result is not None:
            return update_result

        # Si no existia, error 404
        raise HTTPException(status_code=404, detail=f"Tasca {id} no trobada")

    # Si no has enviat res, te torne igualment la tasca actual
    if (existing := await task_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing

    # I si tampoc existix, pues 404
    raise HTTPException(status_code=404, detail=f"Tasca {id} no trobada")


# ------------------------------------------------------------------------ #
#                           DELETE                                         #
# ------------------------------------------------------------------------ #

# Ací es on fem desaparèixer una tasca del mapa
@app.delete("/tasques/{id}", response_description="Eliminar una tasca")
async def delete_tasca(id: str):
    delete_result = await task_collection.delete_one({"_id": ObjectId(id)})

    # Si s'ha eliminat una, tornem 204, que es lo correcte
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Si no existia, pues error
    raise HTTPException(status_code=404, detail=f"Tasca {id} no trobada")
