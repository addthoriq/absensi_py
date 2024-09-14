#!/bin/sh
# This script checks if the container is started for the first time.

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    # place your script that you only want to run on first startup.
    poetry run alembic upgrade head && poetry run python cli.py initial-data && poetry run uvicorn --host 0.0.0.0 --port 8000 main:app --reload
else
    # script that should run the rest of the times (instances where you 
    # stop/restart containers).
    poetry run uvicorn --host 0.0.0.0 --port 8000 main:app --reload
fi