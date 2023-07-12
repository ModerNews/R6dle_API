import asyncio
import secrets
import hashlib
import datetime
import time
import random

from typing import Annotated, Optional
from random import choice

import requests

from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from database import Database

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()


@router.get('/token')
async def token(request:Request, background_tasks: BackgroundTasks):
    """
    Generates a token for the user identification, and registers new entry in the database

    So, this isn't a safe solution, as it enables session hijacking and spoofing,
    lets one user report multiple times by simply changing the token, etc.
    But what we need it for is only to gather simple statistical data, so it shouldn't be an issue.

    :return: New identification token
    """
    token = secrets.token_urlsafe(64)
    background_tasks.add_task(register_user, token, request)
    return {"token": token}


async def register_user(token, request):
    """
    Registers new user in the database

    :param token: user identification token
    :return:
    """
    request.app.db.add_new_user(token)


@router.get("/")
async def root():
    return {}


@router.get("/stats/global")
async def daily_stats(request: Request, date: Optional[datetime.date] = None):
    """
    Gets the daily stats counter

    :param request: representation of the request sent by the user
    :param date: Optional parameter to get the stats for a specific day, if empty, gets defaults to today
    :return:
    """
    return {"message": request.app.db.get_daily_results()[1] if not date else request.app.db.get_daily_results(date.strftime("%Y-%m-%d"))[1]}


@router.get("/stats/user")
async def user_stats(request: Request, token: Annotated[str, Depends(oauth_2_scheme)]):
    current_user_stats = request.app.db.get_user(token)
    return {"message": {"max_streak": current_user_stats[2],
                        "current_streak": current_user_stats[3],
                        "total_solves": current_user_stats[4]} if current_user_stats else "User not found"}


@router.patch("/stats")
async def daily_stats_setter(request: Request, solves: str, token: Annotated[str, Depends(oauth_2_scheme)]):
    """
    Updates the daily stats counter with the new solve

    :param request: representation of the request sent by the user
    :param solves: number of guesses it took to solve the challenge
    :param token: user identification token
    :return:
    """
    try:
        current_stats = request.app.db.get_daily_results()[1]
        current_stats[solves] += 1
    except TypeError:  # If none stats available
        current_stats = {solves: 1}
    except KeyError:  # If the number of guesses is not in the database
        current_stats[solves] = 1

    # TODO custom error, so it doesn't flag other TypeErrors falsely
    try:
        current_user_stats = list(request.app.db.get_user(token))
    except TypeError:  # If none stats available
        request.app.db.add_new_user(token)
        current_user_stats = list(request.app.db.get_user(token))


    current_user_stats = caculate_updated_user_stats(current_user_stats)

    request.app.db.update_user(current_user_stats)
    request.app.db.update_daily_results(current_stats)
    return {"message": "OK"}

def caculate_updated_user_stats(current_user_stats):
    current_user_stats[4] += 1
    if current_user_stats[5] == datetime.datetime.utcnow().date() - datetime.timedelta(days=1):
        current_user_stats[3] += 1
    else:
        current_user_stats[3] = 1

    if current_user_stats[3] > current_user_stats[2]:
        current_user_stats[2] = current_user_stats[3]

    current_user_stats[5] = datetime.datetime.utcnow().date().strftime("%Y-%m-%d")
    return current_user_stats

def get_new_daily_op():
    """
    Generates a new daily operator

    Function sets the seed to the current date, so that the operator changes daily and is the same for all users.
    :return:
    """
    random.seed(datetime.datetime.utcnow().strftime("%Y-%m-%d"))
    data = [key for key, value in requests.get(
        "https://raw.githubusercontent.com/rwlodarczyk/rwlodarczyk.github.io/master/src/r6dle/r6ops.json").json().items()]
    return choice(data)


@router.get("/operator")
async def daily_operator(token: Annotated[str, Depends(oauth_2_scheme)]):
    return {"operator": hashlib.sha256(get_new_daily_op().encode('ascii')).hexdigest()}
