# Download base image
FROM ubuntu:18.04

# Set variables
ARG APP_DIR=/usr/src/app
ARG PORT=5000

# Update Software repository, install package and clean the package
RUN apt-get update  && \
    apt-get install -y --no-install-recommends python3-pip python3-dev build-essential nano &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the flask script into the container and set the working directory
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}
COPY server.py test.py ./

# Copy the requirements file in to image for pip download
COPY requirements.txt ./

# Run install tensorflow, niftynet, flask
RUN pip3 install --upgrade pip setuptools
RUN pip3 install wheel
RUN pip3 install -r requirements.txt

# Install abdominal model
RUN net_download dense_vnet_abdominal_ct_model_zoo

# Remove the sample nifti data from the download model so image will take your input instead
RUN rm -rf /root/niftynet/data/dense_vnet_abdominal_ct/*

# Copy the config to the container to replace the defautl sample config file
COPY config.ini /root/niftynet/extensions/dense_vnet_abdominal_ct/

EXPOSE ${PORT}

# Set the entry point to the script so when we start the docker it will run the server
ENTRYPOINT ["gunicorn"]

# Start server
CMD ["--workers","4","--bind", "0.0.0.0:5000", "server:app"]
