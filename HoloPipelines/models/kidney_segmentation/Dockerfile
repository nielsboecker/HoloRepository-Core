# Download base image
FROM ubuntu:18.04

# Set variables
ARG APP_DIR=/usr/src/app
ARG PORT=5001

# Update Software repository, install package and clean the package
RUN apt-get update  && \
    apt-get install -y --no-install-recommends python3-pip python3-dev build-essential nano &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the flask script into the container and set the working directory
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}
COPY server.py model.py test.py ./

# Copy the requirements file in to image for pip download
COPY requirements.txt ./

# Copy the model into the container
copy kidney_model_miscnn ./

# Run install packages
RUN pip3 install --upgrade pip setuptools
RUN pip3 install wheel
RUN pip3 install -r requirements.txt

# Create data folder for predictions
RUN mkdir -p ${APP_DIR}/data

EXPOSE ${PORT}

# Set the entry point to the script so when we start the docker it will run the server
ENTRYPOINT ["gunicorn"]

# Start server
CMD ["--workers","4","--bind", "0.0.0.0:5000", "server:app"]
