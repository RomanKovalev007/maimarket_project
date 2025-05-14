from django.shortcuts import render

def main_page(request):
    return render(request, 'main/index.html')

def support(request):
    return render(request, 'main/support.html')

