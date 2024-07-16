#!/bin/bash
alembic upgrade head
poetry run python app/__main__.py