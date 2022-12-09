from decimal import Decimal
from django.forms import ModelChoiceField, ModelForm, Textarea, URLInput


from .models import Post


class PostForm(ModelForm):
    
        class Meta:
            model = Post
            fields = ['post']
            exclude = ['author','likes']
            widgets = {
                'post': Textarea(attrs={
                    'class': "form-control",
                    'autofocus': 'true',
                    'style':  ' height: 20em; resize: none;' ,
                    'placeholder': 'Whats On Your Mind',
                    'required': 'True'
                    })
            }