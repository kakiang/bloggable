from django import forms
from .models import Comment

from tinymce import TinyMCE

from django.utils.translation import gettext_lazy as _

# class TinyMCEWidget(TinyMCE):
#     def use_required_attribute(self, *args):
#         return False


class CommentForm(forms.ModelForm):
    # content = forms.CharField(widget=TinyMCE(mce_attrs={'width': 750,'height':300}))
    # content = forms.CharField(
    #     widget = TinyMCEWidget(
    #         attrs={'required':False,'cols':30,'rows':5}
    #     )
    # )

    class Meta:
        model = Comment
        fields = ['content',]
        widgets = {'content':forms.Textarea(attrs={'rows': 5}),}
        labels = {'content': _(''),}


class SearchForm(forms.Form):
    term = forms.CharField(label='')


class SharePostEmailForm(forms.Form):
    subject = forms.CharField(max_length=150)
    message = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(max_length=70)
    sender = forms.EmailField()
    recipient = forms.EmailField()
    # cc_myself = forms.BooleanField(required=False)
