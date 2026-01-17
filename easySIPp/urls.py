from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('xml/<str:xmlname>', views.serve_xml_file, name='xml-file'),
    path('edit-xml/', views.xml_editor, name='edit-xml'),
    path('sipp/<str:xml>/<int:pid>', views.sipp_screen, name='display_sipp_screen'),
    path('xml-management/', views.xml_mgmt_view, name='xml-management'),
    path('create-scenario-xml/', views.create_scenario_xml_view, name='create_scenario_xml'),
]