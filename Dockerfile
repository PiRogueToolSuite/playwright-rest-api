FROM mcr.microsoft.com/playwright/python:v1.32.0-focal
ARG APP_HOME=/app

COPY ./requirements.txt ${APP_HOME}/requirements.txt
RUN pip install --no-cache-dir --upgrade -r ${APP_HOME}/requirements.txt

RUN addgroup --system alice && adduser --system --ingroup alice alice

COPY --chown=alice:alice ./app ${APP_HOME}/app

RUN python --version

USER alice
WORKDIR ${APP_HOME}
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]