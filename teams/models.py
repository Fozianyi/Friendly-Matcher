from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Team(models.Model):
    SKILLS_LEVEL = [
        ('Professional', 'Professional: Football is a career'),
        ('Unprofessional', 'Unprofessional: Participate in tournaments'),
        ('Hobbyist', 'Hobbyist: Play for fun and exercise'),
    ]
    name = models.CharField(max_length=200)
    coach = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    web = models.URLField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(null=True, blank=True, upload_to='images/')
    has_pitch = models.BooleanField(default=False)
    skills_level = models.CharField(
        max_length=20,
        choices=SKILLS_LEVEL,
        default='Select Skills Level'
        )
    location =models.CharField(max_length= 200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Match(models.Model):
    MATCH_STATUS_PENDING = 'pending'
    MATCH_STATUS_APPROVED = 'approved'
    MATCH_STATUS_REJECTED = 'Rejected'
    MATCH_STATUS_CHOICES = [
        (MATCH_STATUS_PENDING, 'Pending'),
        (MATCH_STATUS_APPROVED, 'Approved'),
        (MATCH_STATUS_REJECTED, 'Rejected'),
    ]

    
    date = models.DateField()
    kick_off = models.TimeField(max_length=5)
    my_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='my_team')
    opponent = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='opponent')
    venue =models.CharField(max_length= 200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=MATCH_STATUS_CHOICES, default=MATCH_STATUS_PENDING)
    
    def __str__(self):
        return f'{self.my_team.name} vs. {self.opponent.name} ({self.date}, {self.kick_off})'

class MatchResult(models.Model):
    match = models.OneToOneField('Match', on_delete=models.CASCADE, related_name='result')
    my_team_score = models.PositiveIntegerField()
    opponent_score = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.my_team_score}:{self.opponent_score}"

class PendingApproval(models.Model):
    APPROVAL_CHOICES = (
        ('approve', 'Approve'),
        ('reject', 'Reject')
    )
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='pending_approvals')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pending_approvals_created')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pending_approvals_approved', null=True, blank=True)
    rejected_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pending_approvals_rejected', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approval = models.CharField(max_length=20, choices=APPROVAL_CHOICES, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('match', 'created_by')


class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)