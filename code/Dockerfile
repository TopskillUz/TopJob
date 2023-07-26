FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN echo "$PWD"
#RUN ls

WORKDIR /my_code
COPY . /my_code/

# Install Poetry
RUN apt clean && apt update && apt install curl netcat vim -y
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN #echo "$PWD"

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock* /my_code/

ENV PYTHONPATH "${PYTHONPATH}:/my_code/app"

RUN poetry install
RUN echo "Successfully installed required packages"

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh