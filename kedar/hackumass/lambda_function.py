import json
import boto3
import os

rekognition_client = boto3.client('rekognition')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Get bucket and object key from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    try:
        # Call Rekognition to detect faces and emotions
        response = rekognition_client.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            Attributes=['ALL']
        )

        # Extract emotions from the first face detected (if any)
        emotions = []
        if response['FaceDetails']:
            emotions = response['FaceDetails'][0]['Emotions']
        
        # Format emotions for readability
        detected_emotions = {emotion['Type']: emotion['Confidence'] for emotion in emotions}

        print(f"Detected emotions: {json.dumps(detected_emotions)}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(detected_emotions)
        }
    
    except Exception as e:
        print(f"Error processing object {key} from bucket {bucket}. Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
