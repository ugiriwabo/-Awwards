from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404
import datetime as dt
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile,Project

@login_required(login_url='/accounts/login/')
def welcome(request):
    current_user=request.user
    profile=Profile.objects.get(user=current_user.id)
    images=Profile.get_profile(profile.user_id)
    return render(request,'welcome.html',{'profile':profile,'images':images})

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
        return redirect('welcome')

    else:
        form = ProfileForm()
    return render(request, 'profile.html', {"form": form})

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'user' in request.GET and request.GET["bio"]:
        search_term = request.GET.get("user")
        searched_users = Image.search_by_user(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"users": searched_users})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})