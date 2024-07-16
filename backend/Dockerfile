FROM python:3.12.4-bullseye

RUN pip install poetry \
    && apt-get update -y \
    && apt-get install -y ffmpeg libsm6 libxext6 \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR .
COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi


CMD alembic upgrade head ; poetry run python app/__main__.py
