from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from database import Database

from main import router


class App(FastAPI):
    """
    Main application class for all API calls
    """
    def __init__(self):
        super().__init__()  # Initiate FastAPI
        self.mount("/static", StaticFiles(directory="../static"), name="static")
        self.db = Database()  # Initiate database connection

        self.include_router(router)  # Mount main router from main.py
        self._configure_cors()  # Enable strict CORS policy

    def _configure_cors(self):
        """
        This is helper function to configure CORS policy
        All changes to CORS should be made here

        This uses the CORSMiddleware provided by FastAPI

        Currently, CORS is limited only to old R6dle domain
        :return:
        """
        origins = [
            "https://rwlodarczyk.github.io", "*r6dle.tech", "*"
        ]

        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )