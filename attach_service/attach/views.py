from django.shortcuts import render

from .forms import APILogsForm

# Create your views here.
def index(request):
    return render(request, "attach/index.html")

def api_log(request):
    if request.method == 'POST':
        pass
    else:
        form = APILogsForm()
    return render(request, 'attach/logs.html', {'form': form})