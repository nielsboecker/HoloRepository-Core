FROM node:11.12.0-alpine

ARG SRC_APP_DIR=./server
ARG TARGET_APP_DIR=/usr/src/app
ARG PORT=3006

# Prepare directories
RUN mkdir -p ${TARGET_APP_DIR}
WORKDIR ${TARGET_APP_DIR}

# Install production dependencies
COPY ${SRC_APP_DIR}/package*.json ./
RUN npm install 

# Compile app
COPY ${SRC_APP_DIR} .


EXPOSE ${PORT}
CMD ["npm", "run", "start"]
