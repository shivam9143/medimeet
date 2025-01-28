from rest_framework import serializers


class BaseResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.JSONField(required=False, allow_null=True)
    error = serializers.CharField(required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Automatically set a default status code if none provided
        self.context['code'] = self.context.get('code', 200)
