import boto3
from fastapi import HTTPException
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv
load_dotenv()
s3_client = boto3.client('s3', region_name='us-east-1')

BUCKET_NAME = os.getenv('S3_BUCKET')
def get_s3_url(s3_key: str) -> str:
    """
    Genera la URL pública de un archivo en S3.
    """
    try:
        public_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        return public_url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="No credentials available to access S3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating URL: {str(e)}")