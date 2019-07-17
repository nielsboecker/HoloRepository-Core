FROM aw0905/niftynet:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential nano
COPY . /app
WORKDIR /app
RUN pip install flask
COPY ./niftynet /root/niftynet
ENTRYPOINT ["python"]
CMD ["app.py"]
