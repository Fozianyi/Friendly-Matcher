from django.shortcuts import render, redirect
from . models import Team, Match, MatchResult, PendingApproval, Notification
from django.contrib import messages
from .forms import TeamForm, MatchForm, MatchApprovalForm, MatchResultForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import datetime,  timedelta, date
#from datetime import timezone
import calendar
from calendar import monthrange, HTMLCalendar
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
# Create your views here.

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.created_by = request.user
            team.save()
            return redirect('team-details', team_id=team.id)
    else:
        form = TeamForm()
    return render(request, 'teams/create_team.html', {'form': form})


def team_details(request, team_id):
    team = Team.objects.get(id=team_id)
    return render(request, 'teams/team_details.html', {'team':team})

def update_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('team-details', team_id=team.id)
    else:
        form = TeamForm(instance=team)
    return render(request, 'teams/update_team.html', {'form': form, 'team': team})



def list_teams(request):
    team_list = Team.objects.all()
    query = request.GET.get('q')
    if query:
        team_list = team_list.filter(Q(name__icontains=query) | 
                                     Q(location__icontains=query) | 
                                     Q(skills_level__icontains=query))
    p = Paginator(team_list, 10)
    page = request.GET.get('page')
    teams = p.get_page(page)
    nums = "a" * teams.paginator.num_pages
    return render(request, 'teams/list_team.html', 
                  {'team_list': team_list,
                   'teams': teams,
                   'nums': nums,
                   'query': query}
                 )

@login_required
def user_teams(request):
    teams = Team.objects.filter(created_by=request.user)
    return render(request, 'teams/user_teams.html', {'teams': teams})


def search_teams(request):
    query = request.GET.get('q')
    if query:
        teams = Team.objects.filter(Q(name_icontains=query) | Q(locationicontains=query) | Q(skills_level_icontains=query))
    else:
        teams = Team.objects.all()

    # Render search results as HTML
    html = render_to_string('teams/search_results.html', {'teams': teams, 'query': query})

    # Return search results as JSON
    return JsonResponse({'html': html})


@login_required
def schedule_match(request):
    my_team = get_object_or_404(Team, created_by=request.user)
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.created_by = request.user
            match.status = Match.MATCH_STATUS_PENDING
            match.save()
            # Check if the opponent has approved the match
            opponent = match.opponent.created_by
            if opponent == request.user:
                # The user is the opponent, so automatically approve the match
                match.status = Match.MATCH_STATUS_APPROVED
                match.save()
            else:
                # The user is not the opponent, so create a pending approval record
                pending_approval = PendingApproval.objects.create(match=match, created_by=opponent)
                messages.success(request, 'Match proposed successfully, waiting for approval')
            #create_notification(Match.opponent.created_by, f"You have a new match against {Match.my_team} on {Match.date}.")    
            return redirect('view_match', match_id=match.id)
    else:
        form = MatchForm(initial={'my_team': my_team})  # Set the initial value of my_team to the team created by the logged-in user
    return render(request, 'teams/schedule_match.html', {'form': form})

def update_schedule_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.method == "POST":
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('view_match', match_id=match.id)
    else:
        form = MatchForm(instance=match)
    #create_notification(Match.created_by, f"Your match with {Match.opponent} has been updated.")
    return render(request, 'teams/update_schedule_match.html', {'form': form})



def view_match(request, match_id):
    match = Match.objects.get(id=match_id)
    return render(request, 'teams/view_match.html', {'match': match})

@login_required
def approve_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    
    # Make sure the user is the opponent for this match
    if match.opponent.created_by != request.user:
        messages.error(request, 'You are not authorized to approve this match')
        return redirect('view_match', match_id=match.id)
    
    if request.method == 'POST':
        if 'approve' in request.POST:
            match.status = Match.MATCH_STATUS_APPROVED
            match.save()
            messages.success(request, 'Match approved')
            
            # Delete any pending approval record for this match
            PendingApproval.objects.filter(match=match).delete()
            
        elif 'reject' in request.POST:
            match.status = Match.MATCH_STATUS_REJECTED
            match.save()
            messages.success(request, 'Match rejected')
        return redirect('view_match', match_id=match.id)
    
    return render(request, 'teams/approve_match.html', {'match': match})


@login_required
def pending_approval_matches(request):
    # Retrieve all pending approval records for matches created by the user
    pending_approval_records = PendingApproval.objects.filter(created_by=request.user)

    # Retrieve the matches associated with each pending approval record
    pending_approval_matches = [p.match for p in pending_approval_records]

    # Filter out matches that have been approved or rejected
    approved_matches = Match.objects.filter(status=Match.MATCH_STATUS_APPROVED)
    rejected_matches = Match.objects.filter(status=Match.MATCH_STATUS_REJECTED)
    pending_approval_matches = [m for m in pending_approval_matches if m not in approved_matches and m not in rejected_matches]

    return render(request, 'teams/pending_approvals.html', {'matches': pending_approval_matches})

def upcoming_matches(request):
    # Get all approved matches
    matches = Match.objects.filter(status=Match.MATCH_STATUS_APPROVED).order_by('date')

    if request.method == 'POST':
        match_id = request.POST.get('match_id')
        match = get_object_or_404(Match, id=match_id)
        # validate and save the match result
        form = MatchResultForm(request.POST, match=match)
        if form.is_valid():
            result = form.save(commit=False)
            result.match = match
            result.save()
            messages.success(request, 'Match result added successfully.')
            return redirect('view_match', match_id=match_id)
    else:
        form = MatchResultForm()

    return render(request, 'teams/fixtures.html', {'matches': matches, 'form': form})


def calendar_view(request):
    approved_approvals = PendingApproval.objects.filter(approval='approved')
    approved_matches = [approval.match for approval in approved_approvals]
    matches_info = [{'my_team': match.my_team, 'opponent': match.opponent, 'date': match.date, 'kick_off': match.kick_off, 'venue': match.venue} for match in approved_matches]
       # Get the current month and year
    today = date.today()
    year = today.year
    month = today.month
    
    # Get the calendar for the current month
    cal = calendar.monthcalendar(year, month)
    
    # Get the matches for the current month
    matches = Match.objects.filter(date__year=year, date__month=month)
    
    # Add the matches to the calendar
    for week in cal:
        for i, day in enumerate(week):
            if day != 0:
                matches_on_day = matches.filter(date__day=day)
                week[i] = {'day': day, 'matches': matches_on_day}

    #Get the dates for the games
    game_dates =[match.date.day for match in matches]
    
    # Get the previous and next months
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if prev_month != 12 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if next_month != 1 else year + 1
    
    return render(request, 'teams/calender.html', {'cal': cal, 'year': year, 'month': month, 'prev_month': prev_month, 'prev_year': prev_year, 'next_month': next_month, 'next_year': next_year, 'today': today, 'matches':matches, 'game_dates':game_dates})

@login_required
def approved_matches(request):
    # Get the team created by the current logged-in user
    team = Team.objects.get(created_by=request.user)

    # Get the approved matches for the team
    approved_approvals = PendingApproval.objects.filter(approval='approved', match__my_team=team)
    approved_matches = [approval.match for approval in approved_approvals]

    # Construct a list of match information to display in the template
    matches_info = [{'my_team': match.my_team, 'opponent': match.opponent, 'date': match.date, 'kick_off': match.kick_off, 'venue': match.venue} for match in approved_matches]

    return render(request, 'teams/approved_matches.html', {'matches_info': matches_info})

def team_approved_matches(request, team_id):
    # Get the team object with the given ID
    team = get_object_or_404(Team, id=team_id)

    # Get the approved matches for the team
    approved_approvals = PendingApproval.objects.filter(approval='approved', match__my_team=team)
    approved_matches = [approval.match for approval in approved_approvals]
    #approved_matches = Match.objects.filter(Q(my_team=team) | Q(opponent=team), approval='approved')

    return render(request, 'teams/approved_matches.html', {'team': team, 'approved_matches': approved_matches})

def team_rejected_matches(request, team_id):
    # Get the team object with the given ID
    team = get_object_or_404(Team, id=team_id)

    # Get the rejected matches for the team
    approved_approvals = PendingApproval.objects.filter(approval='rejected', match__my_team=team)
    rejected_matches = [approval.match for approval in approved_approvals]
    #rejected_matches = Match.objects.filter(Q(home_team=team) | Q(away_team=team), is_approved=False)

    # Construct a list of match information to display in the template
    #matches_info = [{'my_team': match.my_team, 'opponent': match.opponent, 'date': match.date, 'kick_off': match.kick_off, 'venue': match.venue} for match in approved_matches]

    return render(request, 'teams/rejected_matches.html', {'team': team, 'rejected_matches': rejected_matches})


def view_calendar(request, year, month):
    try:
         year = int(year)
         month = int(month)
    except ValueError:
         return HttpResponseBadRequest("Invalid year or month value")
        
    first_day = date(int(year), int(month), 1)
    last_day = monthrange(first_day.year, first_day.month)[1]
    last_day = date(int(year), int(month), last_day)


    now = datetime.now()
    time = now.strftime('%I:%M %p')

    matches = Match.objects.filter(start_time__year=year, start_time__month=month)

    next_month = first_day + timedelta(days=32)
    prev_month = first_day - timedelta(days=1)

    return render(request, 'teams/view_calendar.html', {
        'matches': matches,
        'time': time,
        'first_day': first_day,
        'last_day': last_day,
        'next_month': next_month,
        'prev_month': prev_month,
        'notification': 'No matches scheduled this month.' if not matches else ''
    })

def show_calendar(request, year=None, month=None):
    if year and month:
        year = int(year)
        month = int(month)
    else:
        now = datetime.now()
        year = now.year
        month = now.month

    cal = calendar.HTMLCalendar(firstweekday=calendar.SUNDAY)
    month_cal = cal.formatmonth(year, month)

    now =datetime.now()
    current_year = now.year

    matches = Match.objects.filter(date__year=year, date__month= month)
    time = now.strftime('%I:%M %p')


    return render(request, 'teams/calendar.html', {'month_cal': month_cal, 'month': month, 'year': year, 'current_year':current_year, 'time':time , 'matches':matches  })


@login_required
def add_match_result(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    # check if the match date and time is in the past
    match_datetime = datetime.combine(match.date, match.kick_off)
    if match_datetime > datetime.now():
        messages.error(request, 'Cannot add match result for future matches.')
        return redirect('view_match', match_id=match_id)

    # check if the user is authorized to add match results
    if request.user != match.my_team.created_by and request.user != match.opponent.created_by and request.user not in match.opponent.members.all():
        messages.error(request, 'You are not authorized to add match result for this match.')
        return redirect('view_match', match_id=match_id)

    if request.method == 'POST':
        # validate and save the match result
        form = MatchResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.match = match
            result.save()
            messages.success(request, 'Match result added successfully.')
            return redirect('view_match', match_id=match_id)
    else:
        form = MatchResultForm()

    context = {
        'match': match,
        'form': form,
    }
    return render(request, 'result.html', context)


def create_notification(user, message):
    Notification.objects.create(user=user, message=message, timestamp=timezone.now())

