# syntax=docker/dockerfile:1

FROM python:3.14-alpine3.23 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache postgresql-client postgresql-dev

RUN pip install --quiet uv
ENV UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# development
FROM builder AS development

ENV PATH="/app/.venv/bin:$PATH"

COPY . .
EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py seed_accounts && python manage.py runserver 0.0.0.0:8000"]

# production
FROM python:3.14-alpine3.23 AS production

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

RUN apk add --no-cache postgresql-client

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY . .

EXPOSE 8000
CMD ["gunicorn", "ModuleManagerProject.wsgi:application", "--bind", "0.0.0.0:8000"]