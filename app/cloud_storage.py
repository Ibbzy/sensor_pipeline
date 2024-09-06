from google.cloud import storage
import os

def upload_to_gcs(local_file_path, bucket_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    os.remove(local_file_path)
    return f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"
