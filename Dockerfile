FROM python:3.11

WORKDIR /src

RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install --no-cache-dir --upgrade pip  \
    && pip3 install --no-cache-dir poetry \
    &&poetry config virtualenvs.create false

COPY src/poetry.lock .
COPY src/pyproject.toml .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

COPY src/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh && \
    chmod +x /entrypoint.sh

COPY src .

CMD ["/entrypoint.sh"]