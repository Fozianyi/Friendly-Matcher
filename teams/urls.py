from .import views
from django.urls import path

urlpatterns = [
    path('list-teams', views.list_teams, name="list-teams"),
	path('create-team', views.create_team, name='create-team'),
	path('team/<int:team_id>', views.team_details, name='team-details'),
	#path('show_venue/<venue_id>', views.show_venue, name='show-venue'),	
	path('search-teams', views.search_teams, name='search-teams'),
	#path('update-details/<team_id>', views.update_details, name='update-details'),
	path('<int:team_id>/update/', views.update_team, name='update-team'),
	path('user/', views.user_teams, name='user-teams'),
	path('schedule/', views.schedule_match, name='schedule_match'),
    path('view/<int:match_id>/', views.view_match, name='view_match'),
   	path('calendar/<int:year>/<int:month>/', views.show_calendar, name='show_calendar'),
    path('calendar/', views.show_calendar, name='show_calendar'),
	path('calender/', views.calendar_view, name='calendar_view'),
	path('<int:match_id>/update_schedule_match/', views.update_schedule_match, name='update_schedule_match'),
	path('fixtures', views.upcoming_matches, name ='fixtures'),
	path('matches/<int:match_id>/add_result/', views.add_match_result, name='add_result'),
	path('pending_approvals', views.pending_approval_matches, name = 'pending_approvals'),
	#path('pending-approvals/<int:approval_id>/', views.pending_approval_detail, name='pending_approval_detail'),
	#path('pending-approval/approve/<int:approval_id>/', views.pending_approval_approve, name='pending_approval_approve'),
	#path('pending-approvals/<int:approval_id>/reject/', views.pending_approval_reject, name='pending_approval_reject'),
	path('team/<int:team_id>/approved-matches/', views.approved_matches, name='approved_matches'),
	path('teams/search/', views.search_teams, name='search-teams'),
	path('teams/<int:team_id>/approved-matches/', views.team_approved_matches, name='approved_matches'),
    path('teams/<int:team_id>/rejected-matches/', views.team_rejected_matches, name='rejected_matches'),
    path('notifications', views.create_notification, name='notifications'),
    path('match/approve/<int:match_id>/', views.approve_match, name='approve_match'),

	
] 