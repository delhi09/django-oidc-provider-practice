from django import forms


class AuthorizeForm(forms.Form):
    response_type = forms.CharField(max_length=100)
    scope = forms.CharField(max_length=100)
    client_id = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    redirect_uri = forms.CharField(max_length=100)
    nonce = forms.CharField(max_length=100)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    response_type = forms.CharField(max_length=100)
    scope = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    redirect_uri = forms.CharField(max_length=100)
    nonce = forms.CharField(max_length=100)


class ConsentForm(forms.Form):
    consented = forms.BooleanField()

class TokenForm(forms.Form):
    grant_type = forms.CharField(max_length=100)
    code = forms.CharField(max_length=100)
    redirect_uri = forms.CharField(max_length=100)
    client_id = forms.CharField(max_length=100)
    client_secret = forms.CharField(max_length=100)
