from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def profie_list_view(request):
    context = {
        "object_list": User.objects.filter(is_active=True)
    }
    return render(request, "profiles/list.html", context)

@login_required
def profile_view(request, username=None, *args, **kwargs):
    user = request.user
    print(
        user.username,
        user.has_perm("subscriptions.basic"),
        user.has_perm("subscriptions.pro"),
        user.has_perm("subscriptions.advanced"),
    )
    user_groups = user.groups.all()
    # print("user_groups", user_groups)
    # if user_groups.filter(name__icontains='basic').exists():
    #     return HttpResponse("Congrats")
    profile_user_object = get_object_or_404(User, username=username)
    return HttpResponse(f"Hello There {username} - {profile_user_object.id}")