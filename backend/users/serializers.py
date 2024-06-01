from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def get_user_by_email(self, data):
        try:
            return User.objects.get(user_email__iexact=data['user_email'])
        except User.DoesNotExist:
            return None
