from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from typing import Union


from model import Recipe

router = APIRouter()


@router.post("/", response_description="Create new recipe", status_code=status.HTTP_201_CREATED, response_model=Recipe)
async def createRecipe(request: Request, recipe: Recipe = Body(...)):
    recipe = jsonable_encoder(recipe)
    newRecipe = request.app.database["recipes"].insert_one(recipe)
    createdRecipe = request.app.database["recipes"].find_one(
        {"_id": newRecipe.inserted_id}
    )

    return createdRecipe


@router.get("/", response_description="List all recipes with type and category filters if needed", response_model=List[Recipe])
async def getAll(request: Request, type: Union[str, None] = None, category: Union[str, None] = None):

    recipes = request.app.database["recipes"]

    cursor = filterDocuments(recipes, type, category)

    list = []

    for doc in cursor:
        list.append(doc)

    return list


@router.get("/random", response_description="Retrieve a random recipe with type and category optional query parameters", response_model=Recipe)
async def getRandomSnack(request: Request, type: Union[str, None] = None, category: Union[str, None] = None):

    recipes = request.app.database["recipes"]

    operator = {"$sample": {"size": 1}}

    cursor = filterDocuments(recipes, type, category, operator)

    return cursor.next()


def filterDocuments(recipes, type, category, operator=None):
    query = {}

    if (type):
        query["mealType"] = type

    if (category):
        query["mealCategory"] = category

     # This match stage will return matching documents if <type> and/or <category> have a value, otherwise matches all documents
    pipeline = [{"$match": query}]

    if (operator):
        pipeline.append(operator)

    # The aggregate method returns results as a CommandCursor which is basically an iterator class
    # The sample pipeline command extracts <size> random documents from the collection
    cursor = recipes.aggregate(pipeline)

    return cursor
