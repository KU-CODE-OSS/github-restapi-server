import httpx
import json
from datetime import datetime
from multiprocessing import Process

# --- FAST API ---#
from fastapi import Response
from fastapi import FastAPI

# --- API LIST ---#
import api.user.main as user
import api.repos.main as repos

# --- settings --- #
from settings import *

app = FastAPI()
app.include_router(user.router)
app.include_router(repos.router)

#--- ROOT ----#
@app.get("/home")
async def root():

    return {"message": "Welcome to the FastAPI application"}
#--- ---#