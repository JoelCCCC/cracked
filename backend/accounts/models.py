from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user so we can hang gamification state off the auth model."""

    display_name = models.CharField(max_length=60, blank=True)
    total_xp = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_active_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def name(self):
        return self.display_name or self.username

    @property
    def rank(self):
        """Cosmetic title derived from XP. Ordered low -> high."""
        for threshold, title in reversed(RANKS):
            if self.total_xp >= threshold:
                return title
        return RANKS[0][1]

    def touch_streak(self, today):
        """Advance the daily streak. Call once per scored submission."""
        if self.last_active_on == today:
            return False
        if self.last_active_on and (today - self.last_active_on).days == 1:
            self.current_streak += 1
        else:
            self.current_streak = 1
        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_active_on = today
        return True


RANKS = [
    (0, "Script Kiddie"),
    (250, "Junior"),
    (750, "Builder"),
    (1500, "Engineer"),
    (3000, "Senior"),
    (5000, "Architect"),
    (8000, "Cracked"),
]
