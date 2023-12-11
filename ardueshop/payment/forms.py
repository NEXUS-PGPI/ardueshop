from django import forms


class SaveDataForm(forms.Form):
    save_data_checkbox = forms.BooleanField(required=False, initial=True)
