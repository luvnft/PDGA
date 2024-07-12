from django import forms

class PlayerNumberForm(forms.Form):
    player_number = forms.CharField(
        label='Player Numbers',
        widget=forms.TextInput(attrs={'placeholder': 'Enter up to 8 player PDGA numbers separated by commas'}),
        max_length=70
    )

    def clean_player_number(self):
        data = self.cleaned_data['player_number']
        player_numbers = [num.strip() for num in data.split(',')]
        
        # Limit the number of player numbers to 8
        if len(player_numbers) > 8:
            raise forms.ValidationError("You can only search for up to 8 player numbers at a time.")
        
        return data