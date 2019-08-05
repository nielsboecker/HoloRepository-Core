# Niftynet abdominal neural network container
This page describes how to create a docker image that is with the endpoint for the network described in

Eli Gibson, Francesco Giganti, Yipeng Hu, Ester Bonmati, Steve Bandula, Kurinchi Gurusamy, Brian Davidson, Stephen P. Pereira, Matthew J. Clarkson and Dean C. Barratt (2017), Automatic multi-organ segmentation on abdominal CT with dense v-networks https://doi.org/10.1109/TMI.2018.2806309

This network model container segments eight organs on abdominal CT, comprising the gastointestinal tract (esophagus, stomach, duodenum), the pancreas, and nearby organs (liver, gallbladder, spleen, left kidney).

Here is the repo for the network model
https://github.com/NifTK/NiftyNetModelZoo/tree/5-reorganising-with-lfs/dense_vnet_abdominal_ct
the repo only runs in the niftynet framework so to run the network model locally you need to follow the isntruction from the niftynet and download the framework first
https://niftynet.readthedocs.io/en/dev/installation.html


## Build Docker image from the Docker file

```
# example
docker build -t niftynet .
```

This instruction will create the niftynet docker image with flask server end point. to run the image you create you need to run the other command


## run docker and connect docker to the port 5000 
```
# example
docker run --rm -d -p 5000:5000 --name="niftynet" niftynet
```


This instruction will link your local port 5000 with the port 5000 in the container and the container has been seted to run the server when it you run the docker image

now we can send the request to the container because server is running, Here I use curl to send a post request with the file i would like to segement and send it to the container. when container recieve this input nifti file it will call the NN model to segement the input file and when process is complete the flask server will find the output file and return it to the client.

### API
Here i use flask framework to run my gunicorn server so i have a local port that allow user to send request to the container, container can accept the segment request input and output it to the user.
The container runs on the ```http://localhost:5000```
to send a request for the segmentation, We provide a ```/model``` endpoint to do the segmentation.

Here are the requirements for the segmentation request:
* request must send to this address ```http://localhost:5000/model```
* request must be a post request
* request should contains the nifiti file you would like to segment
* the format for the nifiti file should  end with .nii format
* to reuse this container you might need to modify the config file depends on your nifiti input, further infomation about how to modify the config file you can find out from the niftynet website https://niftynet.readthedocs.io/en/dev/config_spec.html

Here is an example that i use curl to send a post request to the container

```
curl -X POST -F file=@100_CT.nii http://localhost:5000/model -o output.nii.gz
```

### Testing for the flask script
To run the test, you need to make sure that you docker container is ruuning and you can run this command 

```
docker exec niftynet python3 test.py
```
