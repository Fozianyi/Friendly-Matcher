from django.views.generic import ListView
from .models import Team, Match, MatchResult, PendingApproval, Notification
from django import forms
from django.forms import ModelForm
from django.utils import timezone


class TeamForm(ModelForm):
	class Meta:
		model = Team
		fields = ('name', 'coach', 'contact_person', 'phone_number', 'web',  'email', 'logo', 'has_pitch','location','skills_level','description')
		#labels = {
		#	'name': '',
		#	'coach': '',
		#	'contact_person': '',
		#	'phone_number': '',
		#	'web': '',
		#	'email': '',
		#	'logo': '',	
        #   'description': '',			
		#}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Team Name'}),
			'coach': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Team Coach'}),
			'contact_person': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Contact Person'}),
			'phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone_Number'}),
			'web': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Web Address'}),
			'email_address': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
		}

class MatchForm(forms.ModelForm):
	class Meta:
		model = Match
		fields =('date', 'kick_off', 'my_team', 'opponent','venue')
		widgets = {
			'date': forms.TextInput(attrs={'type':'date', 'placeholder':'start_time'}),
			'kick_off': forms.TimeInput(attrs={'type': 'text', 'placeholder': 'Kick Off', 'pattern': '[0-9]{2}:[0-9]{2}'}),

		}

class MatchResultForm(forms.ModelForm):
    class Meta:
        model = MatchResult
        fields = ('my_team_score', 'opponent_score')
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        match = self.instance.match
        self.fields['my_team_score'].label = match.my_team.name
        self.fields['opponent_score'].label = match.opponent.name


class MatchApprovalForm(forms.ModelForm):
    APPROVAL_CHOICES = (
        ('approve', 'Approve'),
        ('reject', 'Reject')
    )
    approval = forms.ChoiceField(choices=APPROVAL_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = PendingApproval
        fields = ('approval', 'comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
			
        }
        
class NotificationListView(ListView):
    model = Notification

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-timestamp")