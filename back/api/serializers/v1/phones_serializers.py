from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import TelephonesModel
from index.models import UserRequestsList


class PhoneListSerializer(serializers.ListSerializer):
    def save(self, **kwargs):
        request = UserRequestsList(
            validate_data=[valid_data.get('phone') for valid_data in self.validated_data],
            user=kwargs['user'],
            request_type=UserRequestsList.RequestType.PHONE_REQUEST,
        )
        request.save()
        return request


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=50)

    class Meta:
        list_serializer_class = PhoneListSerializer


class PhoneResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelephonesModel
        fields = ('number', 'filepath', 'text')


class PhonePaginatorSerializer(serializers.Serializer):
    number = serializers.CharField()
    count = serializers.IntegerField()
    results = PhoneResponseSerializer(many=True)


class UserResponseSerializer(serializers.Serializer):
    request_id = serializers.UUIDField()
    data = PhonePaginatorSerializer(many=True)


class ExtraParamsSerializer(serializers.ModelSerializer):
    page_id = serializers.IntegerField()

    def validate(self, attrs):
        if attrs['number'] not in self.context['request_instance'].validate_data:
            raise ValidationError(_('number not in request'))
        return attrs

    def save(self, user):
        self.context['request_instance'].filter_params[
            self.validated_data['number']
        ] = self.validated_data['page_id']
        if user == self.context['request_instance'].user:
            self.context['request_instance'].save()
        return self.context['request_instance']

    class Meta:
        model = TelephonesModel
        fields = (
            'number',
            'page_id',
        )
