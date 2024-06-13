from django.http  import HttpResponse
from django.shortcuts import render

def home_page_view(request, *args, **kwargs):
    my_title = "Main page"
    myContext = {
        "page_title": my_title
    }
    html_template = "base.html"
    return render(request, html_template,myContext)