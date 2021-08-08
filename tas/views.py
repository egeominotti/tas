from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def websocket(request):
    return render(request, 'testWebSocket.html')
