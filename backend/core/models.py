from django.db import models

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    sport = models.CharField(max_length=50, choices=[("cricket", "Cricket"), ("football", "Football"), ("basketball", "Basketball"), ("tennis", "Tennis"), ("badminton", "Badminton"), ("chess", "Chess")], default="cricket")
    format = models.CharField(max_length=50, choices=[("league", "League"), ("knockout", "Knockout"), ("round_robin", "Round Robin")], default="league")
    teams = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("registration", "Registration"), ("ongoing", "Ongoing"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="registration")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    prize_pool = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255)
    tournament_name = models.CharField(max_length=255, blank=True, default="")
    captain = models.CharField(max_length=255, blank=True, default="")
    players = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("eliminated", "Eliminated"), ("disqualified", "Disqualified")], default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Match(models.Model):
    tournament_name = models.CharField(max_length=255)
    team_a = models.CharField(max_length=255, blank=True, default="")
    team_b = models.CharField(max_length=255, blank=True, default="")
    venue = models.CharField(max_length=255, blank=True, default="")
    date = models.DateField(null=True, blank=True)
    score = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("scheduled", "Scheduled"), ("live", "Live"), ("completed", "Completed"), ("postponed", "Postponed"), ("cancelled", "Cancelled")], default="scheduled")
    winner = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.tournament_name
