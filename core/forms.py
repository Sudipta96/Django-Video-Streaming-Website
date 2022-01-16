from django import forms
from core.models import Video



class ContentCreateForm(forms.ModelForm):
    title = forms.CharField(required=True,
                         widget=forms.TextInput(
                         attrs={
                         'class': 'form-control',
                         'placeholder': 'Write down your content title',
                         }))
    description = forms.CharField(required=True,
                                  widget=forms.Textarea(
                                  attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Write down about your content',
                                  'rows': 5,
                                  'cols': 20,
                                  }))
    class Meta:
        model = Video
        fields = ('title','description','thumbnail','file','catagory')

        widgets = {
              'catagory': forms.Select(attrs={'class':'form-control'}),
        }
