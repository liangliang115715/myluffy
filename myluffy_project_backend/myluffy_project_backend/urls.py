"""myluffy_project_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from api.views.course import CourseView,CourseDetailView,CourseCategoryView
from api.views.login import LoginView
from api.views.logout import LogoutView

from api.views.shoppingcar import ShoppingCarView
from api.views.account import AccountView
from api.views.payment import PaymentView
from api.views.payment import get_pay_url
from api.views.captcha import CaptchaView
from api.views.order import OrderView
from api.views.trade import AlipayTradeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path("logout/",LogoutView.as_view()),

    path('category/',CourseCategoryView.as_view({'get':'list'})),
    re_path('course/(?P<category_id>\d+)/$', CourseView.as_view({'get':'list'})),
    path('course/', CourseView.as_view({'get':'list'})),

    re_path('course/detail/(?P<pk>\d+)/$', CourseDetailView.as_view({'get':'retrieve'})),
    re_path('course/detail/$', CourseDetailView.as_view({'get': 'list'})),


    re_path('shoppingcar/$', ShoppingCarView.as_view()),
    re_path('account/$', AccountView.as_view()),
    re_path('payment/$', PaymentView.as_view()),

    re_path("myorder/", OrderView.as_view()),
    re_path("get_pay_url/", get_pay_url),
    re_path("api/v1/trade/alipay/", AlipayTradeView),

    path('captcha_verify/',CaptchaView.as_view())

]
