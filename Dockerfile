FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

LABEL org.opencontainers.image.source="https://github.com/PiRogueToolSuite/playwright-rest-api" \
      org.opencontainers.image.description="Playwright REST API service for URL screenshot and traffic capture" \
      org.opencontainers.image.vendor="Defensive Lab Agency" \
      org.opencontainers.image.licenses="GPL-3.0"

ARG APP_HOME=/app

COPY ./requirements.txt ${APP_HOME}/requirements.txt
RUN pip install --no-cache-dir --upgrade -r ${APP_HOME}/requirements.txt

RUN addgroup --system alice && adduser --system --ingroup alice alice

COPY --chown=alice:alice ./app ${APP_HOME}/app

RUN python --version

RUN playwright install firefox

USER alice
WORKDIR ${APP_HOME}
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]