#!/bin/bash

echo "Create S3 Bucket..."
awslocal s3 mb s3://selected-element-html-s3-bucket

echo "List S3 Buckets..."
awslocal s3 ls
