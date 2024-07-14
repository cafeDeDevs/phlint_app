import logging
import boto3

logger = logging.getLogger(__name__)


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
