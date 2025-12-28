from django.shortcuts import render

def home(request):
    return render(request, 'base.html')

def post_job(request):
    return render(request, 'jobs/post_job.html')


