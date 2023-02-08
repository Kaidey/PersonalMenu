import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Recipe(BaseModel):

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    ingredients: list = Field(...)
    name: str = Field(...)
    mealCategory: str = Field(...)
    mealType: str = Field(...)
    preparation: str = Field(...)

    class Config:

        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Tosta de ovos mexidos com pesto e tomate",
                "ingredients": ["tomate", "ovos", "pesto", "pão"],
                "mealCategory": "Veggie",
                "mealType": "Snack",
                "preparation": "Cook eggs, toast slice of bread, spread pesto on bread, place eggs on bread, top with sliced cherry tomatoes"
            }
        }
