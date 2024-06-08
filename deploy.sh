#!/bin/bash

# Define variables
FUNCTION_NAME="my_lambda_function"
ZIP_FILE="function.zip"
HANDLER="function.lambda_handler"
ROLE_ARN="arn:aws:iam::123456789012:role/my-lambda-role"
RUNTIME="python3.8"
TIMEOUT=30

# Go to /function folder
cd function

# Install requirements and pack the Python function
pip install -r requirements.txt -t .  
zip -r ../$ZIP_FILE .  

# Go to main directory
cd ..

# Verify if lambda function already exists
aws lambda get-function --function-name $FUNCTION_NAME

if [ $? -eq 0 ]; then
  echo "Updating existing function..."
  aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://$ZIP_FILE
else
  echo "Creating new function..."
  aws lambda create-function \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://$ZIP_FILE \
    --handler $HANDLER \
    --runtime $RUNTIME \
    --role $ROLE_ARN \
    --timeout $TIMEOUT
fi

# Remove zip file after upload
rm $ZIP_FILE  