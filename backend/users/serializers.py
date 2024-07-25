from rest_framework import serializers
from users.models import User, Albums, Photos, Networks



class EmailRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def get_user_by_email(self, data) -> User | None:
        try:
            return User.objects.get(user_email__iexact=data['user_email'])
        except User.DoesNotExist:  # type:ignore
            return None


class AlbumsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Albums
        fields = '__all__'


class PhotosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photos
        fields = '__all__'


class NetworksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Networks
        fields = '__all__'
