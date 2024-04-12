#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1
cd /home/app

poetry install


poetry run python -m app.main.queue &

sleep 5

poetry run uvicorn app.main.main:app --host=0.0.0.0 --port=80 --reload
