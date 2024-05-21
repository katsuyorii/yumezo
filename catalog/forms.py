from django import forms
from django.forms import ModelForm
from .models import Comment
        
class AddNewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['review_text', 'grade']

class EditCommentForm(ModelForm):
    review_text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'product-detail-reviews-textarea',
        'placeholder': 'Оставьте комментарий...',
    }), label=None)

    class Meta:
        model = Comment
        fields = ['review_text', 'grade']