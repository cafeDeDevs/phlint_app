import base64
import logging
import boto3

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.utils.s3_utils import *


@api_view(['GET'])
@permission_classes([AllowAny])
def get_gallery_test(request, backend) -> Response:
    # TODO: grab user_name using request.user to query db
    # and use that instead of the email to name default s3 directory,
    # we'll need Google OAuth Signup/Onboarding to do this
    s3_client = boto3.client('s3')
    try:
        file_list = grab_file_list()
        image_files = []

        # TODO: Don't rely on this, refactor to create new buckets instead of directories
        if len(file_list) == 0:
            upload_file('./users/assets/default.jpg', 'phlint-app-s3-test',
                        'default.jpg')

        for file in file_list:
            # NOTE: Creates a default album/file if first time seeing gallery
            if f'{request.user}/default/' not in file:
                upload_file('./users/assets/default.jpg', 'phlint-app-s3-test',
                            f'{request.user}/default/default.jpg')
        for file in file_list:
            if f'{request.user}/default/' in file:
                file_obj = s3_client.get_object(Bucket='phlint-app-s3-test',
                                                Key=file)
                image_data = base64.b64encode(
                    file_obj['Body'].read()).decode('utf-8')
                image_files.append(image_data)

        # Use this once buckets are used
        #  return Response({'message': 'No Images In Your Gallery Found.'},
        #  status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                'message':
                'Images Retrieved From S3 And Sent To Client Successfully.',
                'imagesAsBase64': image_files
            },
            status=status.HTTP_200_OK)
    except Exception as e:
        logging.error(e)
        return Response(
            {
                'message':
                'An Error Occurred While Trying To Retrieve Your Gallery'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
