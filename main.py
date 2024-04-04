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
import api.repos.contributor.main as contributor
import api.repos.issue.main as issue
import api.repos.pull.main as pull
import api.repos.commit.main as commit

# --- settings --- #
from settings import *

app = FastAPI()
app.include_router(user.router)
app.include_router(repos.router)
app.include_router(contributor.router)
app.include_router(issue.router)
app.include_router(pull.router)
app.include_router(commit.router)

#--- ROOT ----#
@app.get("/home")
async def root():

    return {"message": "Welcome to the FastAPI application"}
#--- ---#