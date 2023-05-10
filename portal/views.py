from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .scripts.cpu_stress import main as cpu_stress
import socket
import os


@api_view(['GET'])
def api_status(request):
    text = "server Ok"
    return Response(text, status=status.HTTP_200_OK)


def index_view(request):
    remote_ip = request.META.get('REMOTE_ADDR')
    host_name = socket.gethostname()

    try:
        secret_file = open('./secret.yml', 'r')
        secret = secret_file.read()
    except Exception as err:
        secret = f'Error read file\n {err}'

    try:
        config_file = open('./config.yml', 'r')
        config = config_file.read()
    except Exception as err:
        config = f'Error read file\n {err}'

    secret_env = os.environ.get('SECRET_ENV')
    context = {
        'host_name': host_name,
        'secret_file': secret,
        'secret_env': secret_env,
        'config_file': config,
        'remote_ip': remote_ip
    }

    return render(request, 'index.html', context)


def page1_view(request):
    return render(request, 'page1.html')


def stress_view(request):
    if request.method == 'POST' and 'strs_btn' in request.POST:
        cpu_stress()

    return render(request, 'stress.html')


def headers_view(request):

    context = {
        'headers': request.headers
    }

    return render(request, 'headers.html', context)
