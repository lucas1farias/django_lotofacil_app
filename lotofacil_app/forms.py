

from django import forms
from .models import *


class NewGameModelForm(forms.ModelForm):
    class Meta:
        model = NewGame
        fields = ('game_text',)
        game_text = forms.CharField(max_length=100)

    def show_object_data(self):
        print('Valor do input recebido: ', self.cleaned_data['game_text'], type(self.cleaned_data['game_text']))
