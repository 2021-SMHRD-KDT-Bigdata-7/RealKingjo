from django import forms
from LogosBoard.models import TAd, TCivil, TCriminal, TCriminalSummary, TFamily, TLaw, TLog


class lawform(forms.Form):
    context = forms.CharField(max_length=255)
    brother = forms.CharField(max_length=255)
    subject = forms.CharField(widget=forms.Textarea)
    content = forms.CharField(widget=forms.Textarea)
    keyword = forms.CharField(widget=forms.Textarea)
    abst = forms.CharField(widget=forms.Textarea)
    law = forms.CharField(widget=forms.Textarea)

