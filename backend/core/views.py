import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Tournament, Team, Match


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['tournament_count'] = Tournament.objects.count()
    ctx['tournament_cricket'] = Tournament.objects.filter(sport='cricket').count()
    ctx['tournament_football'] = Tournament.objects.filter(sport='football').count()
    ctx['tournament_basketball'] = Tournament.objects.filter(sport='basketball').count()
    ctx['tournament_total_prize_pool'] = Tournament.objects.aggregate(t=Sum('prize_pool'))['t'] or 0
    ctx['team_count'] = Team.objects.count()
    ctx['team_active'] = Team.objects.filter(status='active').count()
    ctx['team_eliminated'] = Team.objects.filter(status='eliminated').count()
    ctx['team_disqualified'] = Team.objects.filter(status='disqualified').count()
    ctx['match_count'] = Match.objects.count()
    ctx['match_scheduled'] = Match.objects.filter(status='scheduled').count()
    ctx['match_live'] = Match.objects.filter(status='live').count()
    ctx['match_completed'] = Match.objects.filter(status='completed').count()
    ctx['recent'] = Tournament.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def tournament_list(request):
    qs = Tournament.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(sport=status_filter)
    return render(request, 'tournament_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def tournament_create(request):
    if request.method == 'POST':
        obj = Tournament()
        obj.name = request.POST.get('name', '')
        obj.sport = request.POST.get('sport', '')
        obj.format = request.POST.get('format', '')
        obj.teams = request.POST.get('teams') or 0
        obj.status = request.POST.get('status', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.prize_pool = request.POST.get('prize_pool') or 0
        obj.save()
        return redirect('/tournaments/')
    return render(request, 'tournament_form.html', {'editing': False})


@login_required
def tournament_edit(request, pk):
    obj = get_object_or_404(Tournament, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.sport = request.POST.get('sport', '')
        obj.format = request.POST.get('format', '')
        obj.teams = request.POST.get('teams') or 0
        obj.status = request.POST.get('status', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.prize_pool = request.POST.get('prize_pool') or 0
        obj.save()
        return redirect('/tournaments/')
    return render(request, 'tournament_form.html', {'record': obj, 'editing': True})


@login_required
def tournament_delete(request, pk):
    obj = get_object_or_404(Tournament, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/tournaments/')


@login_required
def team_list(request):
    qs = Team.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'team_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def team_create(request):
    if request.method == 'POST':
        obj = Team()
        obj.name = request.POST.get('name', '')
        obj.tournament_name = request.POST.get('tournament_name', '')
        obj.captain = request.POST.get('captain', '')
        obj.players = request.POST.get('players') or 0
        obj.wins = request.POST.get('wins') or 0
        obj.losses = request.POST.get('losses') or 0
        obj.draws = request.POST.get('draws') or 0
        obj.points = request.POST.get('points') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/teams/')
    return render(request, 'team_form.html', {'editing': False})


@login_required
def team_edit(request, pk):
    obj = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.tournament_name = request.POST.get('tournament_name', '')
        obj.captain = request.POST.get('captain', '')
        obj.players = request.POST.get('players') or 0
        obj.wins = request.POST.get('wins') or 0
        obj.losses = request.POST.get('losses') or 0
        obj.draws = request.POST.get('draws') or 0
        obj.points = request.POST.get('points') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/teams/')
    return render(request, 'team_form.html', {'record': obj, 'editing': True})


@login_required
def team_delete(request, pk):
    obj = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/teams/')


@login_required
def match_list(request):
    qs = Match.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(tournament_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'match_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def match_create(request):
    if request.method == 'POST':
        obj = Match()
        obj.tournament_name = request.POST.get('tournament_name', '')
        obj.team_a = request.POST.get('team_a', '')
        obj.team_b = request.POST.get('team_b', '')
        obj.venue = request.POST.get('venue', '')
        obj.date = request.POST.get('date') or None
        obj.score = request.POST.get('score', '')
        obj.status = request.POST.get('status', '')
        obj.winner = request.POST.get('winner', '')
        obj.save()
        return redirect('/matches/')
    return render(request, 'match_form.html', {'editing': False})


@login_required
def match_edit(request, pk):
    obj = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        obj.tournament_name = request.POST.get('tournament_name', '')
        obj.team_a = request.POST.get('team_a', '')
        obj.team_b = request.POST.get('team_b', '')
        obj.venue = request.POST.get('venue', '')
        obj.date = request.POST.get('date') or None
        obj.score = request.POST.get('score', '')
        obj.status = request.POST.get('status', '')
        obj.winner = request.POST.get('winner', '')
        obj.save()
        return redirect('/matches/')
    return render(request, 'match_form.html', {'record': obj, 'editing': True})


@login_required
def match_delete(request, pk):
    obj = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/matches/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['tournament_count'] = Tournament.objects.count()
    data['team_count'] = Team.objects.count()
    data['match_count'] = Match.objects.count()
    return JsonResponse(data)
