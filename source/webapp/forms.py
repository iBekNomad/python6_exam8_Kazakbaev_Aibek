from django import forms
from webapp.models import Product, Review


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")


class ProductForm(forms.ModelForm):
    description = forms.CharField(max_length=2000, required=False, label="Description",
                                  widget=forms.Textarea)
    image = forms.ImageField(required=False, label='image')

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'image']
        widgets = {'category': forms.Select}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {'rating': forms.Select}
