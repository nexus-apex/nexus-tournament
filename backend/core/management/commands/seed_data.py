from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Tournament, Team, Match
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusTournament with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexustournament.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Tournament.objects.count() == 0:
            for i in range(10):
                Tournament.objects.create(
                    name=f"Sample Tournament {i+1}",
                    sport=random.choice(["cricket", "football", "basketball", "tennis", "badminton", "chess"]),
                    format=random.choice(["league", "knockout", "round_robin"]),
                    teams=random.randint(1, 100),
                    status=random.choice(["registration", "ongoing", "completed", "cancelled"]),
                    start_date=date.today() - timedelta(days=random.randint(0, 90)),
                    end_date=date.today() - timedelta(days=random.randint(0, 90)),
                    prize_pool=round(random.uniform(1000, 50000), 2),
                )
            self.stdout.write(self.style.SUCCESS('10 Tournament records created'))

        if Team.objects.count() == 0:
            for i in range(10):
                Team.objects.create(
                    name=f"Sample Team {i+1}",
                    tournament_name=f"Sample Team {i+1}",
                    captain=f"Sample {i+1}",
                    players=random.randint(1, 100),
                    wins=random.randint(1, 100),
                    losses=random.randint(1, 100),
                    draws=random.randint(1, 100),
                    points=random.randint(1, 100),
                    status=random.choice(["active", "eliminated", "disqualified"]),
                )
            self.stdout.write(self.style.SUCCESS('10 Team records created'))

        if Match.objects.count() == 0:
            for i in range(10):
                Match.objects.create(
                    tournament_name=f"Sample Match {i+1}",
                    team_a=f"Sample {i+1}",
                    team_b=f"Sample {i+1}",
                    venue=f"Sample {i+1}",
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    score=f"Sample {i+1}",
                    status=random.choice(["scheduled", "live", "completed", "postponed", "cancelled"]),
                    winner=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Match records created'))
