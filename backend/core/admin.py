from django.contrib import admin
from .models import Tournament, Team, Match

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["name", "sport", "format", "teams", "status", "created_at"]
    list_filter = ["sport", "format", "status"]
    search_fields = ["name"]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "tournament_name", "captain", "players", "wins", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "tournament_name", "captain"]

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ["tournament_name", "team_a", "team_b", "venue", "date", "created_at"]
    list_filter = ["status"]
    search_fields = ["tournament_name", "team_a", "team_b"]
