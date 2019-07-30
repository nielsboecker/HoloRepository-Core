FROM node:11.12.0-alpine

ARG src_app_dir=./server
ARG src_types_dir=./types
ARG target_app_dir=/usr/src/app
ARG target_types_dir=/usr/src/types
ARG port=3001

# Prepare directories
RUN mkdir -p $target_app_dir
WORKDIR $target_app_dir

# Install production dependencies
COPY $src_app_dir/package*.json $target_app_dir/
RUN npm install --only=production

# Copy and compile types
COPY $src_types_dir $target_types_dir
RUN npm install --prefix $target_types_dir --only=production
RUN npm run build --prefix $target_types_dir

# Compile app
COPY $src_app_dir $target_app_dir
RUN npm run compile

# Clean up
RUN rm -rf $target_app_dir/src $target_app_dir/public
RUN rm -rf $target_types_dir

EXPOSE $port
CMD ["npm", "run", "start"]
