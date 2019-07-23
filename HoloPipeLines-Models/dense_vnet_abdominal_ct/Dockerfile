#Download base image ubuntu 18.04
FROM ubuntu:18.04

# Update Software repository
RUN apt-get update  && apt-get clean 

# install package
RUN apt-get install -y --no-install-recommends python3-pip python3-dev build-essential nano



# Copy the flask script in to the container and set the working directory
COPY server.py test.py /app/
WORKDIR /app

# Copy the requirements file in to image for pip download
COPY requirements.txt /app/

# Run install tensorflow, niftynet, flask
RUN pip3 install --upgrade setuptools 
RUN pip3 install wheel
RUN pip3 install -r requirements.txt

# install abdominal model
RUN net_download dense_vnet_abdominal_ct_model_zoo

# Remove the sample nifti data from the download model so image will take your input instead
RUN rm -rf /root/niftynet/data/dense_vnet_abdominal_ct/*

# Copy the config to the container remove the sample config file
COPY config.ini /root/niftynet/extensions/dense_vnet_abdominal_ct/

# set the entry point to the script so when we start the docker it will run the server
ENTRYPOINT ["gunicorn"]

CMD ["-w","4","-b", "0.0.0.0:5000", "server:app"]