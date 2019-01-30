from django import forms
from .models import Comment

from tinymce import TinyMCE

# class TinyMCEWidget(TinyMCE):
#     def use_required_attribute(self, *args):
#         return False

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(mce_attrs={'width': 800}))
    # content = forms.CharField(
    #     widget = TinyMCEWidget(
    #         attrs={'required':False,'cols':30,'rows':5}
    #     )
    # )

    class Meta:
        model = Comment
        fields = ['content',]
