from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from sampleapp.forms import AuthorizeForm, ConsentForm, LoginForm, TokenForm
from sampleapp.models import AuthorizationCode, AuthorizationToken, RelyingParty
from django.contrib.auth.models import User
from django.utils import crypto
import datetime


class IndexView(View):
    def get(self, request):
        return render(request, "index.html", {})


class AuthorizeView(View):
    def get(self, request):
        form = AuthorizeForm(request.GET)
        if not form.is_valid():
            raise ValueError("Invalid form")
        relying_party = get_object_or_404(
            RelyingParty, client_id=form.cleaned_data["client_id"]
        )
        print(relying_party)
        return render(request, "login.html", form.cleaned_data)

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            print(form.errors)
            return render(request, "login.html", form.cleaned_data)
        try:
            user = User.objects.get(
                username=form.cleaned_data["username"], is_active=True
            )
        except User.DoesNotExist:
            return render(request, "login.html", **form.cleaned_data)
        if not user.check_password(form.cleaned_data["password"]):
            return render(request, "login.html", form.cleaned_data)
        authorization_token = crypto.get_random_string(255)
        AuthorizationToken.objects.create(
            token=authorization_token,
            user=user,
            redirect_uri=form.cleaned_data["redirect_uri"],
            state=form.cleaned_data["state"],
            expired_at=datetime.datetime.now() + datetime.timedelta(minutes=10),
        )
        return redirect("sampleapp:consent", authorization_token=authorization_token)


class ConsentView(View):
    def get(self, request, authorization_token):
        return render(request, "consent.html", {"authorization_token": authorization_token})

    def post(self, request, authorization_token):
        form = ConsentForm(request.POST)
        if not form.is_valid():
            return render(request, "consent.html", form.cleaned_data)
        if not form.cleaned_data["consented"]:
            return redirect(authorization_token.redirect_uri)
        authorization_token = get_object_or_404(
            AuthorizationToken, token=authorization_token
        )
        code = crypto.get_random_string(255)
        AuthorizationCode.objects.create(code=code, user=authorization_token.user)
        authorization_token.delete()
        return redirect(
            "{}?code={}&state={}".format(
                authorization_token.redirect_uri, code, authorization_token.state
            )
        )

class TokenView(View):
    def post(self, request):
        form = TokenForm(request.POST)
        if not form.is_valid():
            return render(request, "token.html", form.cleaned_data)
        client = get_object_or_404(RelyingParty, client_id=form.cleaned_data["client_id"])
        # todo check client_secret
        authorization_code = get_object_or_404(
            AuthorizationCode, code=form.cleaned_data["code"]
        )
        access_token = crypto.get_random_string(255)
        token_type = "Bearer"
        refresh_token = crypto.get_random_string(255)
        expires_in = 3600
        id_token_header = {
            "alg": "RS256",
            "typ": "JWT",
        }
        id_token_payload = {
            "iss": "http://localhost:8000",
            "sub": authorization_code.user.username,
            "aud": form.cleaned_data["client_id"],
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=10),
            "nonce": form.cleaned_data["nonce"],
        }
        authorization_code.delete()
