import httpx
import json
from datetime import datetime
from multiprocessing import Process

# --- FAST API ---#
from fastapi import Response
from fastapi import FastAPI

import api.user.main as user
import api.repos.main as repos
import api.contributor.main as contributor
import api.issue.main as issue
import api.pr.main as pr
import api.commit.main as commit
# from api.user import main
# from api.repos import main

# --- settings --- #
from settings import *

app = FastAPI()
app.include_router(user.router)
app.include_router(repos.router)
app.include_router(contributor.router)
app.include_router(issue.router)
app.include_router(pr.router)
app.include_router(commit.router)

#-------------- ROOT ---------------------#
@app.get("/home")
async def root():

    return {"message": "Welcome to the FastAPI application"}
#-----------------------------------------#