"""showops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from login import views

urlpatterns = [
    url('^$', views.Login.as_view()),
	url('^auth/', include('login.urls')),
    url('^itom/', include('itom.urls')),
    url('^flow/', include('flow.urls')),
    # url('^renew/', include('renew.urls')),
]
#错误页面定义
handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.page_error
