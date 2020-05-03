FROM continuumio/miniconda

ARG APP_DIR=/usr/src/app
ARG PORT=3100

RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

COPY requirements.txt ./
COPY environment.yml ./
RUN conda env create -f environment.yml
RUN echo "conda activate idp3" > ~/.bashrc
ENV PATH /opt/conda/envs/idp3/bin:$PATH

RUN cat /etc/os-release
RUN conda info --envs

COPY core ./core
COPY jobs ./jobs
COPY server.py ./
COPY config.py ./

EXPOSE ${PORT}

ENTRYPOINT ["gunicorn"]

# Note: Use only one gunicorn worker as we manually do multiprocessing
# and having multiple workers on gunicorn's end breaks the way we keep
# track of state. May be a candidate for another major refactoring later.
CMD ["--workers","1","--bind", "0.0.0.0:3100", "--timeout", "10000", "server:app"]
