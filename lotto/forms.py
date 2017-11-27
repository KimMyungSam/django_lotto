from django import forms
from .models import FormInput

class LottoForm(forms.ModelForm):

    class Meta:
        model = FormInput
        fields = ('shooter', 'shot_count')
