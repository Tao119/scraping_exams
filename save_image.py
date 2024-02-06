import io
import boto3
import os

from dotenv import load_dotenv
import base64

load_dotenv()


def save_image(data):
    try:

        session = boto3.Session(
            aws_access_key_id=os.getenv('REMODY_AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('REMODY_AWS_SECRET_ACCESS_KEY')
        )
        s3_client = session.client('s3')
        bucket_name = os.getenv("remody-quiz-images")
        file_name = f"selenium_screenshot/{data['image_name']}"

        image_bytes = base64.b64decode(data.get('image'))

        image = io.BytesIO(bytes(image_bytes))

        result = s3_client.put_object(
            Body=image,
            Bucket=bucket_name,
            Key=file_name
        )
        return True
    except Exception as e:
        print(e)
