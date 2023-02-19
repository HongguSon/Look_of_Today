from django import forms

from config.apps.main.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        exclude = ('author',)