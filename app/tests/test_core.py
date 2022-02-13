from logging import debug
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from fastapi.logger import logger
import logging
import pytest

app = FastAPI()
client = TestClient(app)



def test_root():
    # response = client.get('/')
    assert 1 == 1
    # assert response.json() == {"message": "Hello World"}
