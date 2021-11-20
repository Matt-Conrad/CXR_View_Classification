# syntax=docker/dockerfile:1
FROM alpine:3.14
RUN apk add --no-cache python3 g++ make
WORKDIR /CXR_View_Classification
COPY . .
ENTRYPOINT ["/bin/sh"]