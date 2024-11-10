import copy
import boto3
import json
import time
import spotipy 
import os
import cv2
import arduino

# AWS configuration
REGION = "us-east-2"  # Set your region here
BUCKET_NAME = "hackumassbucket4"  # S3 bucket name
LAMBDA_FUNCTION_NAME = "emotionDetectionLambda"  # Lambda function name
IMAGE_FILE_PATH = "javierreyes.png"  # Local path to the image file

# Initialize AWS clients with the specified region
s3_client = boto3.client("s3", region_name=REGION)
lambda_client = boto3.client("lambda", region_name=REGION)

def get_image_from_pi():
    pass

def get_emotion() -> str:
    pass

def spotify(songname, override=False):
    username = os.environ['SP_USERNAME'] 
    clientID = os.environ['SPCLIENTID'] 
    clientSecret = os.environ['SPCLIENTSECRET'] 
    redirect_uri = 'http://google.com/callback/'
    oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri) 
    token_dict = oauth_object.get_access_token() 
    # scope = "user-read-playback-state,user-modify-playback-state"

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
        spotifyObject.repeat('track')


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
    return result
def hex_to_rgb(value):
    value = value.lstrip('#')
    print("tuple", tuple(int(value[i:i+2], 16) for i in (0, 2, 4)))
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

def runmood(lightison, playmusic, img_counter, mappings, device, soundlig):
    if (lightison):
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            return
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        object_name = "opencv_frame_{}.png".format(img_counter)
        
        # Upload the file to S3
        upload_file_to_s3("opencv_frame_{}.png".format(img_counter), BUCKET_NAME, object_name)

        # Wait a bit for the S3 event notification to trigger the Lambda function
        # time.sleep(1)  # Adjust if necessary for your setup

        # Invoke Lambda and get the response
        res = invoke_lambda_and_get_response(BUCKET_NAME, object_name)
        if not res:
            return img_counter
        res = json.loads(res['body'])
        if not res:
            return img_counter
        print("res", res)
        for key in res:
            # print("key", key, res[key])
            res[key] = float(res[key]) / 100.0
        rgb = (0,0,0)
        print("mappings", mappings)
        newmappings = copy.deepcopy(mappings)
        rgbVals = dict()
        for key in newmappings:
            print("key", newmappings[key])
            print("newmappings", newmappings)

            rgbVals[key] = hex_to_rgb(newmappings[key])
            print("rgbVal1s", rgbVals)
            rgbVals[key] = tuple((rgbVals[key][i] * res[key]) for i in range(3))
            print("rgbVawl1s", rgbVals)

            rgb = tuple((rgb[i] + rgbVals[key][i]) for i in range(3))
            
            # print("mappings", newmappings)
        print(rgb, "before")
        rgb = tuple(int(r/8) for r in rgb)
        print(rgb, "rgb")
        if not soundlig:
            arduino.soundModeOff(device)
            arduino.turnOn(device,0,30,rgb[0],rgb[1],rgb[2])
        if soundlig:
            arduino.soundModeOn(device, rgb[0], rgb[1], rgb[2])
        
        
        
        if (playmusic):
            maxkey = max(res, key=res.get)
            if maxkey == "CALM":
                spotify("Clair de Lune")
            elif maxkey == "HAPPY":
                spotify("Best Day of My Life")
            elif maxkey == "SAD":
                spotify("Here Comes the Sun")
            elif maxkey == "ANGRY":
                spotify("Sweden")
            elif maxkey == "SURPRISED":
                spotify("Mr. Brightside")
            elif maxkey == "DISGUSTED":
                spotify("Disgusted")
            elif maxkey == "FEAR":
                spotify("Canon in D")
            else:
                spotify("Lucy in the Sky with Diamonds") #confused
        img_counter += 1
    elif (playmusic):
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            return
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        object_name = "opencv_frame_{}.png".format(img_counter)
        
        # Upload the file to S3
        upload_file_to_s3("opencv_frame_{}.png".format(img_counter), BUCKET_NAME, object_name)
        
        # Wait a bit for the S3 event notification to trigger the Lambda function
        res = invoke_lambda_and_get_response(BUCKET_NAME, object_name)
        res = json.loads(res['body'])
        print("res", res)
        if not res:
            return img_counter
        #get the key of the max value in res:
        maxkey = max(res, key=res.get)
        if maxkey == "CALM":
            spotify("Clair de Lune")
        elif maxkey == "HAPPY":
            spotify("Best Day of My Life")
        elif maxkey == "SAD":
            spotify("Here Comes the Sun")
        elif maxkey == "ANGRY":
            spotify("Sweden")
        elif maxkey == "SURPRISED":
            spotify("Mr. Brightside")
        elif maxkey == "DISGUSTED":
            spotify("Disgusted")
        elif maxkey == "FEAR":
            spotify("Canon in D")
        else:
            spotify("Lucy In The Sky With Diamonds") #confused
        
        # time.sleep(1)
        img_counter += 1
    else:
        img_counter += 1
    return img_counter
        
    # cam = cv2.VideoCapture(0)
    # ret, frame = cam.read()
    # if not ret:
    #     print("failed to grab frame")
    #     break
    # k = cv2.waitKey(1)
    # if k%256 == 27:
    #     # ESC pressed
    #     print("Escape hit, closing...")
    #     break
    # elif k%256 == 32:
    #     # SPACE pressed
    #     img_name = "opencv_frame_{}.png".format(img_counter)
    #     cv2.imwrite(img_name, frame)
    #     print("{} written!".format(img_name))
    #     object_name = "opencv_frame_{}.png".format(img_counter)
        
    #     # Upload the file to S3
    #     upload_file_to_s3("opencv_frame_{}.png".format(img_counter), BUCKET_NAME, object_name)

    #     # Wait a bit for the S3 event notification to trigger the Lambda function
    #     time.sleep(1)  # Adjust if necessary for your setup

    #     # Invoke Lambda and get the response
    #     invoke_lambda_and_get_response(BUCKET_NAME, object_name)
    #     songname = input("song name: ")
    #     spotify(songname)
    #     img_counter += 1

    cam.release()

