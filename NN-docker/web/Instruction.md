## Niftynert abdominal neural network container



### Docker file
The docker file contains all the command for creating the docker images. the image it self contains niftynet and flask. to create the docker image you need to download the repo and go to the directory and enter the command from below

<code>
docker build -t [docker name:tag] .
</code>

This instruction will create the niftynet docker image with flask server end point. to run the image you create you need to run the other command

<code>
## run docker and connect docker to the port 5000 

docker run -d -p 5000:5000 [docker name] 
</code>

This instruction will link your local port 5000 with the port 5000 in the container and the container has been seted to run the server when it you run the docker image

now we can send the request to the container because server is running, Here I use curl to send a post request with the file i would like to segement and send it to the container. when container recieve this input nifti file it will call the NN model to segement the input file and when process is complete the flask server will find the output file and return it to the client.

### Flask script
Here i use flask framework to create a server so i have a port that allow user to send request to the container, container can segment the request input and output it to the user.
### Testing for the flask script
I also wrote some unit testing for the script