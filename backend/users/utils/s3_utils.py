import logging
import boto3
import os

logger = logging.getLogger(__name__)


# NOTE: Potentially Very expensive...
# queries entire bucket every time any user visits to gallery
# TODO: change so that for loop checks for user_name and
# album_name before populating file_list
# NOTE: Maybe creating a new bucket per user isn't such a bad idea after all...
def grab_file_list():
    try:
        file_list = []
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket='phlint-app-s3-test')
        if (response):
            for contents in response['Contents']:
                file_list.append(contents["Key"])
        return file_list
    except Exception as e:
        logger.error("S3 error: %s", str(e))
        return []


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        logging.error(e)
        return False
    return True
