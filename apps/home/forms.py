from django import forms
from captcha.fields import CaptchaField


class AreaCodeForm(forms.Form):
    area_inputData = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "",
                "class": "w-100",
                "rows": 10,
                "cols": 30,
            }
        ))

    capatchacode = CaptchaField(
        generator="apps.authentication.forms.captcha_challenge", error_messages={"invalid": "Verification code error"})
