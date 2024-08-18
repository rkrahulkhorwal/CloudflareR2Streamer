import requests
import boto3
from botocore.client import Config
from urllib.parse import urlparse
import os

def stream_upload_to_r2(url, bucket_name, object_name, endpoint_url, access_key_id, secret_access_key):
    s3 = boto3.client('s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        config=Config(signature_version='s3v4'),
    )

    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    
    # If file size is smaller than 5MB, use single-part upload
    if total_size < 5 * 1024 * 1024:
        print("File is smaller than 5MB. Using single-part upload.")
        body = response.content
        s3.put_object(Bucket=bucket_name, Key=object_name, Body=body)
        print(f"\rUploaded: {len(body)} bytes", flush=True)
    else:
        # For larger files, use multipart upload
        print("File is 5MB or larger. Using multipart upload.")
        mpu = s3.create_multipart_upload(Bucket=bucket_name, Key=object_name)

        try:
            parts = []
            part_number = 1
            bytes_transferred = 0
            chunk_size = 5 * 1024 * 1024  # 5MB chunks

            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    part = s3.upload_part(Body=chunk, Bucket=bucket_name, Key=object_name, 
                                          PartNumber=part_number, UploadId=mpu['UploadId'])
                    
                    parts.append({"PartNumber": part_number, "ETag": part['ETag']})
                    
                    bytes_transferred += len(chunk)
                    part_number += 1

                    # Print progress
                    progress = (bytes_transferred / total_size) * 100
                    print(f"\rProgress: {progress:.2f}% ({bytes_transferred}/{total_size} bytes)", end='', flush=True)

            # Complete the multipart upload
            s3.complete_multipart_upload(Bucket=bucket_name, Key=object_name, 
                                         UploadId=mpu['UploadId'], MultipartUpload={"Parts": parts})
            
            print("\nMultipart upload completed successfully!")

        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            # Abort the multipart upload if there was an error
            s3.abort_multipart_upload(Bucket=bucket_name, Key=object_name, UploadId=mpu['UploadId'])
            raise

def main():
    # Cloudflare R2 configuration
    endpoint_url = 'https://<accountid>.r2.cloudflarestorage.com'
    access_key_id = 'your_access_key_id'
    secret_access_key = 'your_secret_access_key'
    bucket_name = 'your_bucket_name'

    # File to upload
    source_url = input("Enter the URL of the file to upload: ")
    object_name = os.path.basename(urlparse(source_url).path)

    print(f"Streaming upload from {source_url} to R2 bucket {bucket_name}...")
    stream_upload_to_r2(source_url, bucket_name, object_name, endpoint_url, access_key_id, secret_access_key)
    print(f"Uploaded to R2 as {object_name}")

if __name__ == "__main__":
    main()
