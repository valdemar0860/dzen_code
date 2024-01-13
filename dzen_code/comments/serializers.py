import re
from PIL import Image
from rest_framework import serializers
from captcha.fields import CaptchaField

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = '__all__'

    def validate_html_tags(text):
        allowed_tags = ['a', 'code', 'i', 'strong']

        open_tags_pattern = re.compile(r'<(\w+)[^>]*>', re.IGNORECASE)

        close_tags_pattern = re.compile(r'</(\w+)>', re.IGNORECASE)

        open_tags = re.findall(open_tags_pattern, text)
        close_tags = re.findall(close_tags_pattern, text)

        for tag in open_tags:
            if tag not in allowed_tags:
                raise ValueError(f"Using tag {tag} prohibited")

        for tag in close_tags:
            if tag not in allowed_tags:
                raise ValueError(f"Closing tag {tag} prohibited")

        return text

    def validate_image(self, value):
        max_width = 320
        max_height = 240

        image = Image.open(value)
        width, height = image.size

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)

            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
            image = resized_image

        allowed_formats = ['JPEG', 'JPG', 'PNG', 'GIF']
        if image.format not in allowed_formats:
            raise serializers.ValidationError("Acceptable file formats: JPG, GIF, PNG")

        return value
