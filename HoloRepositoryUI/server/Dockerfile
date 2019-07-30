FROM node:11.12.0-alpine

ARG SRC_APP_DIR=./server
ARG SRC_TYPES_DIR=./types
ARG TARGET_APP_DIR=/usr/src/app
ARG TARGET_TYPES_DIR=/usr/src/types
ARG PORT=3001

# Prepare directories
RUN mkdir -p ${TARGET_APP_DIR}
WORKDIR ${TARGET_APP_DIR}

# Install production dependencies
COPY ${SRC_APP_DIR}/package*.json ./
RUN npm install --only=production

# Copy and compile types
COPY ${SRC_TYPES_DIR} ${TARGET_TYPES_DIR}
RUN npm install --prefix ${TARGET_TYPES_DIR} --only=production
RUN npm run build --prefix ${TARGET_TYPES_DIR}

# Compile app
COPY ${SRC_APP_DIR} .
RUN npm run compile

# Clean up
RUN rm -rf ./src ./public
RUN rm -rf ${TARGET_TYPES_DIR}

EXPOSE ${PORT}
CMD ["npm", "run", "start"]
