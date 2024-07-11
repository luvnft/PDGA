from django import forms

class PlayerNumberForm(forms.Form):
    player_number = forms.CharField(
        label='Player Numbers',
        widget=forms.TextInput(attrs={'placeholder': 'Enter player PDGA numbers separated by commas'}),
        max_length=1000
    )