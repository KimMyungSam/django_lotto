from django import forms
from .models import ShootNumbers

class LottoForm(forms.ModelForm):

    class Meta:
        model = ShootNumbers
        fields = ('shooter', 'shoot_lotto')
