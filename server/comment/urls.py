from django.conf.urls import url
from comment import views

urlpatterns = [
    url(r'^$', views.main),
#    url(r'^rout', views.get_network_rout_info),
#    url(r'^nodeinfo', views.get_node_info)
]

