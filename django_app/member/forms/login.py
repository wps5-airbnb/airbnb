from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': '사용자 아이디를 입력하세요',
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력하세요',
            }
        )
    )

    # 유효성 검증을 실행하는 메서드
    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(
            username=username,
            password=password
        )
        # 인증에 성공할 경우 Form의 cleaned_data의 'user'
        # 키에 인증된 MyUser 객체를 할당
        if user is not None:
            self.cleaned_data['user'] = user
        # 인증에 실패한 경우 ValidationError발생시킴
        else:
            raise forms.ValidationError(
                'Your Login Credentials are Not Valid'
            )
        return self.cleaned_data
