#!/bin/sh

# Wait until MinIO server is up
until $(curl --output /dev/null --silent --head --fail http://localhost:9000); do
  echo "Waiting for MinIO server to start..."
  sleep 3
done

# Set up the MinIO alias and create the bucket
mc alias set myminio http://localhost:9000 minioadmin minioadmin
mc mb myminio/selected-element-html-s3-bucket
