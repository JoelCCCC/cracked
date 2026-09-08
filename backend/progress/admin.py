from django.contrib import admin

from .models import ChallengeAttempt, ChallengeSolve, LevelCompletion, TrackCompletion

admin.site.register(ChallengeAttempt)
admin.site.register(ChallengeSolve)
admin.site.register(LevelCompletion)
admin.site.register(TrackCompletion)
