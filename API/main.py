from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as recipeRouter

config = dotenv_values(".env")

app = FastAPI()


@app.on_event("startup")
def startupDbClient():
    app.mongoDbClient = MongoClient(config["ATLAS_URI"])
    app.database = app.mongoDbClient[config["DB_NAME"]]
    print("Connected to the Mongo database!")


@app.on_event("shutdown")
def shutdownDbClient():
    app.mongoDbClient.close()


app.include_router(recipeRouter, tags=["recipes"], prefix="/recipe")
