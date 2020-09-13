from . import views
from django.urls import path

app_name='blog'  # 视图函数命名空间，便于reverse函数解析url
urlpatterns = [
    path('', views.index, name='index'),
    # pk会作为第二个参数传给detail视图函数，其中第一个参数是request
    # <int:pk>,<string:st>等是Django的路由写法
    path('post/<int:pk>',views.detail,name='detail')
]
