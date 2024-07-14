import base64
import logging
import boto3

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.utils.s3_utils import grab_file_list


@api_view(['GET'])
@permission_classes([AllowAny])
def get_gallery_test(request) -> Response:
    s3_client = boto3.client('s3')
    try:
        file_list = grab_file_list()
        image_files = []

        if len(file_list) != 0:
            for file in file_list:
                if '/' in file:
                    file_obj = s3_client.get_object(
                        Bucket='phlint-app-s3-test', Key=file)
                    image_data = base64.b64encode(
                        file_obj['Body'].read()).decode('utf-8')
                    image_files.append(image_data)
        else:
            return Response({'message': 'No Images In Your Gallery Found.'},
                            status=status.HTTP_404_NOT_FOUND)
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
