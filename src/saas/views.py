from django.http  import HttpResponse
from django.shortcuts import render
from visits.models import PageVisit

def home_page_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path = request.path)
    my_title = "Main page"
    myContext = {
        "page_title": my_title,
        "page_visit_count" :page_qs.count(),
        "total_page_count" : qs.count()
    }
    path2 = request.path
    html_template = "home.html"
    PageVisit.objects.create(path = path2)
    return render(request, html_template,myContext)