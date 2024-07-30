from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

# Create your views here.
@login_required
def dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, "dashboard/main.html", {})
    else:
        return HttpResponseBadRequest("Login first")