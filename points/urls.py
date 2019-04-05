from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url('^today/$',views.news_of_day,name='newsToday'),
    url(r'^archives/(\d{4}-\d{2}-\d{2})/$',views.past_days_news,name = 'pastNews'),
    url(r'^profile/', views.my_profile, name='profile'),
    url(r'^view_profile', views.view_profile, name='view_profile'),
    url(r'^upload_project', views.upload_project, name='upload_project'),
    url(r'^search', views.search_project_title, name='search'),
    url(r'^api/project/$', views.ProjectList.as_view()),
    
    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    