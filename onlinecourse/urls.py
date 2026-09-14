from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # ... otras rutas existentes ...
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('<int:course_id>/exam/<int:submission_id>/result/',
         views.show_exam_result, name='show_exam_result'),
]
