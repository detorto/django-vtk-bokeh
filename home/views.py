from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
import requests
import json
from django.conf import settings
#from projects.models import Project
# Create your views here.


@render_to('home.html')
def index(request):
	return {"user":request.user, "current":"home"}
