from django.urls import path

from . import views

# exist for internal app config
# and linking internally

# this urlpatterns name is also fixed
urlpatterns=[
    path("",views.index,name="index"),
    path("start/",views.start,name="start")
    # path("start/",views.index,name="index")
]