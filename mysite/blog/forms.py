from django import forms
from django import forms
from .models import Comment


"""Form to send posts to users email"""
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
        widget=forms.Textarea)

"""Form to accept readers comments"""
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']