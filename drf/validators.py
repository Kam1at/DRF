from rest_framework import serializers


class YouTubeLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'https://www.youtube.com' in value.get('link'):
            return True
        else:
            raise serializers.ValidationError('Wrong link (not YouTube link)')
