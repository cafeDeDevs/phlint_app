import logging
import os
from typing import List

import boto3

logger = logging.getLogger(__name__)


def create_bucket(bucket_name, region=None) -> bool:
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except Exception as e:
        logging.error(e)
        return False
    return True


def delete_bucket(bucket) -> bool:
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_bucket(Bucket=bucket)
    except Exception as e:
        logging.error(e)
        return False
    return True


# TODO: add bucket parameter/argument
def grab_file_list(bucket) -> List[str]:
    try:
        file_list = []
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=bucket)
        if (response):
            for contents in response['Contents']:
                file_list.append(contents["Key"])
        return file_list
    except Exception as e:
        logger.error("S3 error: %s", str(e))
        return []


def upload_file(file_name, bucket, object_name=None) -> bool:
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        logging.error(e)
        return False
    return True


def download_file(file_name, bucket, object_name) -> bool:
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket, object_name, file_name)
    except Exception as e:
        logging.error(e)
        return False
    return True


def delete_file(bucket, key_name) -> bool:
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=bucket, Key=key_name)
    except Exception as e:
        logging.error(e)
        return False
    return True
