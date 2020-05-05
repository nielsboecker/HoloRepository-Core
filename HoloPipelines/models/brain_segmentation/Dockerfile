# Download base image
FROM ubuntu:18.04

# Set variables. Change the port number to the correct port
ARG APP_DIR=/usr/src/app
ARG PORT=5002

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


# Install Requirements
RUN pip3 install --upgrade pip setuptools
RUN pip3 install wheel
RUN pip3 install -r requirements.txt

# Create necessary directories
RUN mkdir data
RUN mkdir prediction
RUN mkdir saved_model

# Copy other necessary files
ADD saved_model ./saved_model
ADD mrbrains ./mrbrains

# Expose the chosen port
EXPOSE ${PORT}

# Set the entry point to the script so when we start the docker it will run the server
ENTRYPOINT ["gunicorn"]

# Start server
CMD ["--workers","1","--bind", "0.0.0.0:5002", "--timeout", "18000", "server:app"]
