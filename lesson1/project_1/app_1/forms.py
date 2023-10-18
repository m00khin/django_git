from django import forms


class UpdateItemForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}),
        label='Описание'
    )
    price = forms.IntegerField(label='Цена')
