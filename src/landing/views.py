from django.shortcuts import render
from visits.models import PageVisit
from dashboard.views import dashboard_view

# Create your views here.
def landing_dashboard_page_view(request):
    qs = PageVisit.objects.all()
    PageVisit.objects.create(path = request.path)
    return render(request, "landing/main.html", {"page_view_count" : qs.count()})