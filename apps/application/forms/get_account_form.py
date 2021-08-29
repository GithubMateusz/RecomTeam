from django import forms


class GetAccountForm(forms.Form):
    account_name = forms.CharField()
