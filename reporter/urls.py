from django.urls import path
from . import views

app_name = 'reporter'

urlpatterns = [
    path("build", views.CreateReport.as_view(), name="create"),
    # Update Files
    path("reports", views.ReportList.as_view(), name="reports"),
    # Update Report
    path('update/<slug>/<int:pk>/', views.UpdateReportView.as_view(), name="report_update"),
    ## Report Detail Pages
    path("<slug>/",views.ReportDetail.as_view(),name="single"),
]
