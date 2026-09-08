from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from curriculum.models import Challenge, Level, Track
from progress.models import ChallengeAttempt, ChallengeSolve, LevelCompletion

DEMO_USERS = [
    {"username": "ada_l", "display_name": "Ada Lovelace", "xp": 8450, "streak": 42},
    {"username": "linus_t", "display_name": "Linus Torvalds", "xp": 7320, "streak": 35},
    {"username": "carmack", "display_name": "John Carmack", "xp": 6500, "streak": 29},
    {"username": "m_hamilton", "display_name": "Margaret Hamilton", "xp": 5200, "streak": 21},
    {"username": "hopper", "display_name": "Grace Hopper", "xp": 3950, "streak": 18},
    {"username": "turing", "display_name": "Alan Turing", "xp": 3300, "streak": 14},
    {"username": "dennis_r", "display_name": "Dennis Ritchie", "xp": 2550, "streak": 11},
    {"username": "ken_t", "display_name": "Ken Thompson", "xp": 1920, "streak": 9},
    {"username": "guido", "display_name": "Guido van Rossum", "xp": 1340, "streak": 7},
    {"username": "dan_a", "display_name": "Dan Abramov", "xp": 880, "streak": 5},
    {"username": "sophie_w", "display_name": "Sophie Wilson", "xp": 520, "streak": 3},
    {"username": "neon_coder", "display_name": "Neon Coder", "xp": 280, "streak": 2},
]


class Command(BaseCommand):
    help = "Seed demo users and leaderboard entries."

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.localdate()
        created_count = 0

        for u_data in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=u_data["username"],
                defaults={
                    "email": f"{u_data['username']}@example.com",
                    "display_name": u_data["display_name"],
                    "total_xp": u_data["xp"],
                    "current_streak": u_data["streak"],
                    "longest_streak": u_data["streak"] + 5,
                    "last_active_on": today,
                },
            )
            if created:
                user.set_password("cracked123")
                user.save()
                created_count += 1
            else:
                user.total_xp = u_data["xp"]
                user.current_streak = u_data["streak"]
                user.last_active_on = today
                user.save()

        # Ensure demo user exists
        demo_user, created = User.objects.get_or_create(
            username="demo",
            defaults={
                "email": "demo@cracked.dev",
                "display_name": "Demo Hacker",
                "total_xp": 105,
                "current_streak": 3,
                "longest_streak": 3,
                "last_active_on": today,
            },
        )
        if created:
            demo_user.set_password("cracked123")
            demo_user.save()
            created_count += 1

            # Give demo user a couple of solved challenges in coding level 1
            first_track = Track.objects.filter(slug="coding").first()
            if first_track:
                first_level = first_track.levels.first()
                if first_level:
                    challenges = list(first_level.challenges.all()[:2])
                    for ch in challenges:
                        ChallengeSolve.objects.get_or_create(
                            user=demo_user,
                            challenge=ch,
                            defaults={"attempts_taken": 1},
                        )
                        ChallengeAttempt.objects.get_or_create(
                            user=demo_user,
                            challenge=ch,
                            defaults={"correct": True, "xp_awarded": ch.xp},
                        )

        self.stdout.write(self.style.SUCCESS(f"Demo data seeded. Total seeded users: {len(DEMO_USERS) + 1}"))
