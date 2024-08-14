import base64
import logging

import boto3
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import User
from users.utils.s3_utils import *


# TODO: denote if user is trying to get default gallery (initial sign in)
# or is trying to get specified gallery (should be in request and/or url)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_gallery_test(request, backend) -> Response:
    # TODO: grab user_name using request.user to query db
    # and use that instead of the email to name default s3 directory,
    # we'll need Google OAuth Signup/Onboarding to do this
    try:
        s3_client = boto3.client("s3")
        if isinstance(request.user, User):
            user = request.user.user_name
        else:
            user = request.user
        # NOTE: Creates New Bucket By User Name (i.e. email),
        # simply errors silently if bucket already exists
        create_bucket(str(user))
        bucket_name = str(user)
        file_list = grab_file_list(bucket_name)
        image_files = []

        # TODO: Establish for every image a thumbnail/mobile/desktop/full version of each image
        # NOTE: If there's nothing in the user's bucket yet,
        # establishes a default gallery(directory) in bucket and uploads a default image
        if len(file_list) == 0:
            upload_file("./users/assets/default.jpg", bucket_name, "default.jpg")

        for file in file_list:
            if "default/" in file:
                file_obj = s3_client.get_object(Bucket=bucket_name, Key=file)
                image_data = base64.b64encode(file_obj["Body"].read()).decode("utf-8")
                image_files.append(image_data)

        # Use this once buckets are used
        #  return Response({'message': 'No Images In Your Gallery Found.'},
        #  status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                "message": "Images Retrieved From S3 And Sent To Client Successfully.",
                "imagesAsBase64": image_files,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        logging.error(e)
        return Response(
            {"message": "An Error Occurred While Trying To Retrieve Your Gallery"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def upload_gallery_test(request, backend) -> Response:
    try:
        if not request.FILES:
            return Response(
                {"message": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
            )
        if isinstance(request.user, User):
            user = request.user.user_name
        else:
            user = request.user

        # Get the first file from the request
        uploaded_file = next(iter(request.FILES.values()))
        bucket_name = str(user)
        # NOTE: Because we don't provide an option_name, the
        # file is uploaded directly to s3 without having to save it on our server
        # NOTE: Also, because we don't provide a gallery_name, it puts the image in default
        # TODO: Use gallery_name argument once establishing different galleries
        success = upload_file(uploaded_file, bucket_name)

        if not success:
            return Response(
                {"message": f"Failed to upload {uploaded_file.name} to S3."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "message": "Images Uploaded to S3 Successfully",
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        logging.error(e)
        return Response(
            {"message": "An Error Occurred While Trying To Upload Image to S3"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
