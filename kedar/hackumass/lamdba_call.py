import boto3
import json
import time
import spotipy 
import os

# AWS configuration
REGION = "us-east-2"  # Set your region here
BUCKET_NAME = "hackumassbucket4"  # S3 bucket name
LAMBDA_FUNCTION_NAME = "emotionDetectionLambda"  # Lambda function name
IMAGE_FILE_PATH = "javierreyes.png"  # Local path to the image file

# Initialize AWS clients with the specified region
s3_client = boto3.client("s3", region_name=REGION)
lambda_client = boto3.client("lambda", region_name=REGION)

def spotify(songname, override=False):
    username = os.environ['SP_USERNAME'] 
    clientID = os.environ['SPCLIENTID'] 
    clientSecret = os.environ['SPCLIENTSECRET'] 
    redirect_uri = 'http://google.com/callback/'
    oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri) 
    token_dict = oauth_object.get_access_token() 

    token = token_dict['access_token'] 
    spotifyObject =  spotipy.Spotify(
            auth_manager=spotipy.SpotifyOAuth(
            client_id=clientID,
            client_secret=clientSecret,
            redirect_uri=redirect_uri,    
            open_browser=False))
    user_name = spotifyObject.current_user() 
    print(json.dumps(user_name, sort_keys=True, indent=4)) 

    results = spotifyObject.search(songname, 1, 0, "track") 
    songs_dict = results['tracks'] 
    song_items = songs_dict['items'] 
    song = song_items[0]['external_urls']['spotify'] 
    songsplit = song.split('/')[-1]
    urisplit = spotifyObject.currently_playing().get('item').get('uri').split(':')[-1]
    print("songsplit:", songsplit, urisplit)
    # print(spotifyObject.currently_playing())
    print(songname.lower(), spotifyObject.currently_playing().get('item').get('name').split(':')[-1].lower())
    if songsplit != urisplit and songname.lower() != spotifyObject.currently_playing().get('item').get('name').split(':')[-1].lower().strip(): #doesnt start replaying the same song if it is already playing
        spotifyObject.start_playback(uris=[song])


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


import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        object_name = "opencv_frame_{}.png".format(img_counter)
        songname = input("song name: ")
        spotify(songname)
        # Upload the file to S3
        upload_file_to_s3("opencv_frame_{}.png".format(img_counter), BUCKET_NAME, object_name)

        # Wait a bit for the S3 event notification to trigger the Lambda function
        time.sleep(1)  # Adjust if necessary for your setup

        # Invoke Lambda and get the response
        invoke_lambda_and_get_response(BUCKET_NAME, object_name)
        img_counter += 1

cam.release()

cv2.destroyAllWindows()