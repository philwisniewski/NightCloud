# sample Dockerfile to test usage when passing in this repo
FROM alpine:3.14

# set working directory
WORKDIR /app

# copy all files
COPY . .

# default command: list files and say hello
CMD ls -lah && echo "Hello from NightCloud"
