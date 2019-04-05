from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404
import datetime as dt
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm,UploadProjectForm
from .models import Profile,Project
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProjectSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly


@login_required(login_url='/accounts/login/')
def welcome(request):
    current_user=request.user
    img = Project.objects.all()
    return render(request,'welcome.html',{'img':img})

def news_of_day(request):
    date = dt.date.today()
    return render(request, 'all-points/today-news.html', {"date": date,})

def convert_dates(dates):

    # Function that gets the weekday number for the date.
    day_number = dt.date.weekday(dates)

    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday',"Sunday"]

    # Returning the actual day of the week
    day = days[day_number]
    return day

# View Function to present news from past days
def past_days_news(request, past_date):

    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_of_day)

    return render(request, 'all-news/past-news.html', {"date": date})

@login_required(login_url='/accounts/login/')
def my_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect('view_profile')

    else:
        form = ProfileForm()
    return render(request, 'profile.html', {"form": form})

@login_required(login_url='/accounts/login/')
def view_profile(request):
    current_user=request.user
    profile=Profile.objects.get(user=current_user.id)
    images=Profile.get_profile(profile.user_id)
    return render(request,'my_profile.html',{'profile':profile,'images':images})

@login_required(login_url='/accounts/login/')
def upload_project(request):
    current_user=request.user
    if request.method == 'POST':
        form = UploadProjectForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('welcome')

    else:
        form = UploadProjectForm()
    return render(request, 'project.html', {"form": form})

@login_required(login_url='/accounts/login/')
def search_project_title(request):
    if 'title' in request.GET and request.GET["title"]:
        search_term = request.GET.get("title")
        titles = Project.search_title(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"titles":titles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

class ProjectList(APIView):
    def get(self, request, format=None):
        all_project = Project.objects.all()
        serializers = ProjectSerializer(all_project, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        permission_classes = (IsAdminOrReadOnly,)
    