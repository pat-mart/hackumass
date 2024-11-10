import boto3
import json
import time

# AWS configuration
REGION = "us-east-2"  # Set your region here
BUCKET_NAME = "hackumassbucket4"  # S3 bucket name
LAMBDA_FUNCTION_NAME = "emotionDetectionLambda"  # Lambda function name
IMAGE_FILE_PATH = "javierreyes.png"  # Local path to the image file

# Initialize AWS clients with the specified region
s3_client = boto3.client("s3", region_name=REGION)
lambda_client = boto3.client("lambda", region_name=REGION)

def upload_file_to_s3(file_path, bucket, object_name):
    """Uploads a file to S3."""
    try:
        s3_client.upload_file(file_path, bucket, object_name)
        print(f"Uploaded {file_path} to s3://{bucket}/{object_name}")
    except Exception as e:
        print(f"Failed to upload file: {e}")

def invoke_lambda_and_get_response(bucket, object_name):
    """Invokes Lambda function and retrieves the emotions detected."""
    try:
        # Define the event to send to Lambda
        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {
                            "name": bucket
                        },
                        "object": {
                            "key": object_name
                        }
                    }
                }
            ]
        }

        # Call Lambda function
        response = lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,
            InvocationType="RequestResponse",  # Waits for response
            Payload=json.dumps(event),
        )

        # Read and parse the response
        payload = response["Payload"].read().decode("utf-8")
        result = json.loads(payload)
        
        # Check if the Lambda function execution was successful
        if response["StatusCode"] == 200 and "statusCode" in result and result["statusCode"] == 200:
            print("Emotions detected:", json.loads(result["body"]))
        else:
            print("Error in Lambda function:", result)
    
    except Exception as e:
        print(f"Failed to invoke Lambda function: {e}")

def main():
    # Define the object name (using the image file name)
    object_name = IMAGE_FILE_PATH.split("/")[-1]

    # Upload the file to S3
    upload_file_to_s3(IMAGE_FILE_PATH, BUCKET_NAME, object_name)

    # Wait a bit for the S3 event notification to trigger the Lambda function
    time.sleep(5)  # Adjust if necessary for your setup

    # Invoke Lambda and get the response
    invoke_lambda_and_get_response(BUCKET_NAME, object_name)

if __name__ == "__main__":
    main()
