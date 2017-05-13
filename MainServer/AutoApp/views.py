from django.http import HttpResponse

from AutoApp.db_filling import fill_database


# Create your views here.


def load(request):
    fill_database()

    return HttpResponse("hello, files loading success")
