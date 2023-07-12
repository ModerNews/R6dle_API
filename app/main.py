import asyncio
import secrets
import hashlib
import datetime
import time
import random

from typing import Annotated, Optional
from random import choice

import requests

from fastapi import APIRouter, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from database import Database

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()


@router.get('/token')
async def token():
    """
    Generates a token for the user identification

    So, this isn't a safe solution, as it enables session hijacking and spoofing,
    lets one user report multiple times by simply changing the token, etc.
    But what we need it for is only to gather simple statistical data, so it shouldn't be an issue.

    :return: New identification token
    """
    return {"token": secrets.token_urlsafe(64)}


@router.get("/")
async def root():
    return {}


@router.get("/stats")
async def daily_stats(request: Request, date: Optional[datetime.date] = None):
    """
    Gets the daily stats counter

    :param request: representation of the request sent by the user
    :param date: Optional parameter to get the stats for a specific day, if empty, gets defaults to today
    :return:
    """
    return {"message": request.app.db.get_daily_results()[1] if not date else request.app.db.get_daily_results(date.strftime("%Y-%m-%d"))[1]}


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
    except TypeError:  # None stats available
        current_stats = {solves: 1}
    finally:
        request.app.db.update_daily_results(current_stats)
        return {"message": "OK"}


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
