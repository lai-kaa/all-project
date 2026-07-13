from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    """用户注册：用户名 + 密码（无强度限制）"""

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class DirectPasswordChangeForm(SetPasswordForm):
    """已登录用户直接设置新密码，无需旧密码"""

    pass


class ForgotPasswordForm(forms.Form):
    """忘记密码：用户名 + 新密码，确认后直接重置"""

    username = forms.CharField(
        label='用户名',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': '请输入用户名'}),
    )
    new_password1 = forms.CharField(
        label='新密码',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label='确认新密码',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username')
        password1 = cleaned.get('new_password1')
        password2 = cleaned.get('new_password2')

        if password1 and password2 and password1 != password2:
            self.add_error('new_password2', '两次输入的密码不一致')

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise ValidationError('用户名不存在，请检查后重试') from None

            cleaned['user'] = user

        return cleaned
