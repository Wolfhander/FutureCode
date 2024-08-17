from django.http import HttpResponse

def page1_view(request):
    return HttpResponse("Страница намбер ван с фразой намбер ван")

def page2_view(request):
    return HttpResponse("Страница намбер ту с фразой намбер ту")