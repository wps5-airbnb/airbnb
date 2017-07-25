from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from member.forms import UserEditForm

User = get_user_model()

__all__ = (
    'profile',
    'profile_edit',
)


def profile(request, user_pk=None):
    # 유저가 로그인하지 않았으며 user_pk도 주어지지 않은 경우( my_profile에 접근하려는 경우)
    if not request.user.is_authenticated and not user_pk:
        # login view로 이동시키며 뒤의 next get parameter에 다시 profile view의 URL을 붙여줌
        login_url = reverse('member:login')
        redirect_url = login_url + '?next=' + request.get_full_path()
        return redirect(redirect_url)

    if user_pk:
        user = get_object_or_404(User, pk=user_pk)
    else:
        user = request.user  # 자신의 프로필을 보여줌

    context = {
        'cur_user': user,
    }
    return render(request, 'member/profile.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        # UserEditForm에 수정할 data를 함께 binding
        form = UserEditForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user,
        )
        # data가 올바를 경우 (유효성 통과)
        if form.is_valid():
            # form.save()를 이용해 instance를 update
            form.save()
            return redirect('member:my_profile')
    else:
        form = UserEditForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'member/profile_edit.html', context)
