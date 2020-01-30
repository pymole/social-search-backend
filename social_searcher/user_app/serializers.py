from rest_framework import serializers
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from .models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_vk_authorized')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()

        mail_subject = 'Активируйте аккаунт.'
        to_email = validated_data.get('email')

        html_content = render_to_string('acc_active_email.html', {
            'user': validated_data['username'],
            'domain': 'http://ec2-3-121-195-2.eu-central-1.compute.amazonaws.com',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(mail_subject, text_content, to=[to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return user
