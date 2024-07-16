FROM python:3.12-alpine

RUN pip install poetry

WORKDIR .
COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi


CMD ["poetry", "run", "python", "app/__main__.py"]
