# Generated by Django 4.1.2 on 2023-04-02 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('kick_off', models.TimeField(max_length=5)),
                ('venue', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('Rejected', 'Rejected')], default='pending', max_length=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('coach', models.CharField(max_length=200)),
                ('contact_person', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('web', models.URLField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('has_pitch', models.BooleanField(default=False)),
                ('skills_level', models.CharField(choices=[('Professional', 'Professional: Football is a career'), ('Unprofessional', 'Unprofessional: Participate in tournaments'), ('Hobbyist', 'Hobbyist: Play for fun and exercise')], default='Select Skills Level', max_length=20)),
                ('location', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MatchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_team_score', models.PositiveIntegerField()),
                ('opponent_score', models.PositiveIntegerField()),
                ('match', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='teams.match')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='my_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_team', to='teams.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='opponent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to='teams.team'),
        ),
        migrations.CreateModel(
            name='PendingApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approval', models.CharField(blank=True, choices=[('approve', 'Approve'), ('reject', 'Reject')], max_length=20, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pending_approvals_approved', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_approvals_created', to=settings.AUTH_USER_MODEL)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_approvals', to='teams.match')),
                ('rejected_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pending_approvals_rejected', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('match', 'created_by')},
            },
        ),
    ]