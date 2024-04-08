from django.forms import ModelForm

from .models import Tweet


class CreateTweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ("content",)
