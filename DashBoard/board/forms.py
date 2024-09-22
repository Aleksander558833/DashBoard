from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Post, Responses
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'author']

    def clean(self):
        clean_data = super().clean()
        title = clean_data.get('title')
        if title is not None and len(title) < 20:
            raise ValidationError({
                'title': 'Заголовок не может быть менее 20 символов.'
            })
        text = clean_data.get('text')
        if text is not None and len(text) < 20:
            raise ValidationError({
                'text': 'Текст не может быть менее 20 символов.'
            })
        return clean_data

class ResponsesForm(forms.ModelForm):
    class Meta:
        model = Responses
        fields = ['text']


