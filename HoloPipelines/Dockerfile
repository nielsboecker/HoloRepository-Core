FROM python:3.7

ARG APP_DIR=/usr/src/app
ARG PORT=3100

RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

COPY requirements.txt ./
RUN pip install gunicorn
RUN pip install -r requirements.txt

COPY core ./core
COPY jobs ./jobs
COPY server.py ./
COPY config.py ./

EXPOSE ${PORT}

ENTRYPOINT ["gunicorn"]

# Note: Use only one gunicorn worker as we manually do multiprocessing
# and having multiple workkers on gunicorn's end breaks the way we keep
# track of state. May be a candidate for another major refactoring later.
CMD ["--workers", "1", "--bind", "0.0.0.0:3100", "server:app"]
