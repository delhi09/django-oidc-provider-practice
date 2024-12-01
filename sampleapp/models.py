from django.db import models


class RelyingParty(models.Model):
    name = models.CharField("名前", max_length=255)
    client_id = models.CharField("クライアントID", max_length=255)
    client_secret = models.CharField("クライアントシークレット", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "リライングパーティ"

class Company(models.Model):
    name = models.CharField("名前", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "企業"

class Contract(models.Model):
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    relying_party = models.ForeignKey("RelyingParty", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "契約"

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_service_available(self, relying_party):
        return Contract.objects.filter(
            company=self.company, relying_party=relying_party
        ).exists()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "従業員"

class AuthorizationToken(models.Model):
    token = models.CharField("トークン", max_length=255)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    redirect_uri = models.CharField("リダイレクトURI", max_length=255)
    state = models.CharField("ステート", max_length=255)
    expired_at = models.DateTimeField("有効期限")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name_plural = "認可トークン"


class AuthorizationCode(models.Model):
    code = models.CharField("コード", max_length=255)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = "認可コード"
