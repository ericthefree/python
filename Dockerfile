# Selecting image
FROM python:3.8.6-alpine3.12

LABEL MAINTAINER="Eric Freeman ericthefree@outlook.com"

ENV GROUP_ID=1000 USER_ID=1000

# Application working directory
WORKDIR /api_app
RUN pwd

# Copying the project files
COPY .  /api_app
COPY .venv /api_app/.venv
RUN ls -la /api_app/*

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

# Exposing our port
EXPOSE 5001

ENV PATH /home/www/.local/bin:$PATH

# Install dependencies - currently controlled in the virtual environment
# COPY /requirements.txt /api_app # requirements.txt should already be in the api_app directory
RUN pip install -r requirements.txt
RUN pip install gunicorn

ENTRYPOINT ["python", "app_start.py"]

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5001", "app_start:api_app"]