FROM oz123/pipenv:3.11-2023.07.4 AS builder
# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1
# Pipfile contains requests
ADD Pipfile.lock Pipfile /usr/src/
WORKDIR /usr/src
RUN pipenv requirements | grep -v rws-common > requirements.txt

FROM python:3.9 AS runtime
RUN apt-get update && apt-get install libsasl2-dev
COPY --from=builder /usr/src/requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

ADD rws-common /usr/src/rws-common
RUN pip install /usr/src/rws-common

ADD . /code
WORKDIR /code
ENV FLASK_ENV=production
CMD exec python -m gunicorn --bind :$PORT --workers 1 --threads 8 identifier:app
