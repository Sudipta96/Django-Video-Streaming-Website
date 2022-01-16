from django import forms
from comment.models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
                        widget=forms.Textarea(
                               attrs={
                               'class': 'form-group form-control',
                               'id': 'content',
                               'rows': 5,
                               'cols': 40
                               }
                        )
                      )
    class Meta:
        model = Comment
        fields = ('content',)

class CommentUpdateForm(forms.ModelForm):
    content = forms.CharField(
                        widget=forms.Textarea(
                               attrs={
                               'class': 'form-group form-control',
                               'id':'content',
                               'rows': 3,
                               'cols': 10,
                               }
                        )
                      )
    class Meta:
        model = Comment
        fields = ('content','status',)
