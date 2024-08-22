from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path("logout/", views.logout, name="logout"),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_register/', views.student_register, name='student_register'),
    path('student_dashboard/student_add/',views.student_add,name='student_add'),
    path('student_dashboard/view_attendance/',views.view_attendance,name='viewattendance'),
    path('student_dashboard/timetable',views.timetables,name='timetable'),
    path('video_feed/',views.video_feed, name="video_feed"),
    path('teacher_dashboard/track/',views.track, name="track"),
    #path('teacher_dashboard/detail/',views.detail, name="detail"),
    path('teacher_dashboard/trackstudent/',views.trackstudent,name='trackstudent'),
    path('teacher_dashboard/traindata/',views.traindata,name='traindata'),
    path('teacher_dashboard/view_attendance/',views.view_t_attendance,name='view_attendance'),
    path('teacher_dashboard/editattendance/<int:id>/',views.edit_attendance,name='edit_attendance'),
    path('teacher_dashboard/timetable',views.timetablet,name='time_table'),
    path('edit_form/<int:attend_id>',views.get_edit_form,name='edit_form'),

]
