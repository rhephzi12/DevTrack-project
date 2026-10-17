from django.urls import path
from issues.views import ReporterListCreateView, IssueListCreateView, IssueDetailView

urlpatterns = [
    path('reporters/', ReporterListCreateView.as_view(), name='reporters'),
    path('issues/', IssueListCreateView.as_view(), name='issues'),
    path('issues/<int:pk>/', IssueDetailView.as_view(), name='issue-detail'),
]
