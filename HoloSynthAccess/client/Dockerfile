# Stage 0
# Front-end build based on Node.js
FROM node:11.12.0-alpine as build-stage

# Static variables
ARG SRC_APP_DIR=./client
ARG TARGET_APP_DIR=/usr/src/app

# Config to be passed at build-time
ARG SYNTH_BACKEND_HOST
ARG SYNTH_BACKEND_PORT
ARG SYNTH_BACKEND_TIMEOUT

# Prepare directories
RUN mkdir -p ${TARGET_APP_DIR}
WORKDIR ${TARGET_APP_DIR}

# Install production dependencies
COPY ${SRC_APP_DIR}/package*.json ./
RUN npm install 

# Compile app
COPY ${SRC_APP_DIR} .
RUN npm run build

################################################################################

# Stage 1
# Production build based on Nginx with artefacts from Stage 0
FROM nginx:1.15.9-alpine

ARG SRC_APP_DIR=./client
ARG TARGET_APP_DIR=/usr/src/app
ARG PORT=3005

COPY ${SRC_APP_DIR}/server-config/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage ${TARGET_APP_DIR}/build /usr/share/nginx/html

EXPOSE ${PORT}

CMD ["nginx", "-g", "daemon off;"]
