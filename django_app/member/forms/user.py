from django import forms

from ..models import MyUser


class UserEditForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = (
            'nickname',
            'img_profile'
        )
