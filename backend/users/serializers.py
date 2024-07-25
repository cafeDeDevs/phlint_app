import logging
from rest_framework import serializers
from users.models import Albums, Networks, Photos, User

logger = logging.getLogger(__name__)



class EmailRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def get_user_by_email(self, data) -> User | None:
        try:
            return User.objects.get(user_email__iexact=data['user_email'])
        except Exception as e:
            logger.error("Error while getting user by email: %s", str(e))
            return None


class AlbumsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Albums
        fields = '__all__'

    def create_album(self, data) -> Albums | None:
        try:
            new_album = Albums(
                title=data['title'],
                s3_url=data['s3_url'],
                is_private=data['is_private'],
                user_id=data['user_id'],
            )
            new_album.save()
            return new_album
        except Exception as e:
            logger.error("Error while creating album: %s", str(e))
            return None


class PhotosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photos
        fields = '__all__'


class NetworksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Networks
        fields = '__all__'
