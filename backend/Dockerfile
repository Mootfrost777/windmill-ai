FROM python:3.10-alpine

RUN pip install poetry

WORKDIR .
COPY . .

RUN poetry env use python3.12 \
    poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi


CMD ["poetry", "run", "python", "app/__main__.py"]