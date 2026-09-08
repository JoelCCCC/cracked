from django.conf import settings
from django.db import models

from curriculum.models import Challenge, Level, Track


class ChallengeAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="attempts", on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, related_name="attempts", on_delete=models.CASCADE)
    submission = models.JSONField(default=dict, blank=True)
    correct = models.BooleanField(default=False)
    xp_awarded = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["user", "challenge"])]


class ChallengeSolve(models.Model):
    """One row per (user, challenge) the first time it is solved."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="solves", on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, related_name="solves", on_delete=models.CASCADE)
    solved_at = models.DateTimeField(auto_now_add=True)
    attempts_taken = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "challenge")


class LevelCompletion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="level_completions", on_delete=models.CASCADE)
    level = models.ForeignKey(Level, related_name="completions", on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "level")


class TrackCompletion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="track_completions", on_delete=models.CASCADE)
    track = models.ForeignKey(Track, related_name="completions", on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "track")
