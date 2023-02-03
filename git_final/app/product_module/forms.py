from django import forms
from django.core import validators
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['parent', 'text']

        widgets = {
            'parent': forms.HiddenInput(attrs={'id': 'parent_id'}),
            'text': forms.Textarea(attrs={'id': 'review_text', 'row': '11', 'required': 'Ture',
                                          'placeholder': 'متن نظر'})

        }

        error_messages = {
            'text': {
                'required': 'متن نظر نمی تواند خالی باشد'
            }
        }
