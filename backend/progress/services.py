"""Progression rules: what is unlocked, what a solve is worth."""

from __future__ import annotations

from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from curriculum.models import Challenge, Level, Track

from .models import ChallengeAttempt, ChallengeSolve, LevelCompletion, TrackCompletion


def solved_challenge_ids(user):
    return set(ChallengeSolve.objects.filter(user=user).values_list("challenge_id", flat=True))


def completed_level_ids(user):
    return set(LevelCompletion.objects.filter(user=user).values_list("level_id", flat=True))


def level_is_unlocked(level, completed_ids, track_unlocked):
    if not track_unlocked:
        return False
    if level.index <= 1:
        return True
    previous = Level.objects.filter(track_id=level.track_id, index=level.index - 1).first()
    return previous is None or previous.id in completed_ids


def build_state(user):
    """One query pass over the whole curriculum, annotated with the user's progress."""
    tracks = (
        Track.objects.prefetch_related("levels")
        .annotate(level_count=Count("levels", distinct=True))
        .order_by("order")
    )
    counts = dict(
        Level.objects.annotate(n=Count("challenges")).values_list("id", "n")
    )
    solved = solved_challenge_ids(user)
    solved_per_level = {}
    for level_id, challenge_id in Challenge.objects.values_list("level_id", "id"):
        if challenge_id in solved:
            solved_per_level[level_id] = solved_per_level.get(level_id, 0) + 1
    completed = completed_level_ids(user)

    payload = []
    for track in tracks:
        track_unlocked = user.total_xp >= track.required_xp
        levels = []
        total_ch = 0
        solved_ch = 0
        for level in track.levels.all():
            total = counts.get(level.id, 0)
            done = solved_per_level.get(level.id, 0)
            total_ch += total
            solved_ch += done
            levels.append(
                {
                    "id": level.id,
                    "index": level.index,
                    "title": level.title,
                    "summary": level.summary,
                    "xp_reward": level.xp_reward,
                    "challenge_count": total,
                    "solved_count": done,
                    "completed": level.id in completed,
                    "unlocked": level_is_unlocked(level, completed, track_unlocked),
                }
            )
        payload.append(
            {
                "id": track.id,
                "slug": track.slug,
                "name": track.name,
                "tagline": track.tagline,
                "description": track.description,
                "icon": track.icon,
                "accent": track.accent,
                "order": track.order,
                "required_xp": track.required_xp,
                "unlocked": track_unlocked,
                "xp_to_unlock": max(0, track.required_xp - user.total_xp),
                "level_count": len(levels),
                "levels_completed": sum(1 for lv in levels if lv["completed"]),
                "challenge_count": total_ch,
                "solved_count": solved_ch,
                "completed": bool(levels) and all(lv["completed"] for lv in levels),
                "levels": levels,
            }
        )
    return payload


@transaction.atomic
def record_submission(user, challenge, submission, correct, detail):
    """Persist the attempt and, on a first solve, pay out XP and unlocks."""
    user = type(user).objects.select_for_update().get(pk=user.pk)
    prior_attempts = ChallengeAttempt.objects.filter(user=user, challenge=challenge).count()
    already_solved = ChallengeSolve.objects.filter(user=user, challenge=challenge).exists()

    xp_awarded = 0
    events = []
    if correct and not already_solved:
        ChallengeSolve.objects.create(user=user, challenge=challenge, attempts_taken=prior_attempts + 1)
        xp_awarded += challenge.xp
        events.append({"type": "challenge", "label": challenge.title, "xp": challenge.xp})

    ChallengeAttempt.objects.create(
        user=user, challenge=challenge, submission=submission, correct=correct, xp_awarded=xp_awarded
    )

    level_completed = False
    track_completed = False
    if correct:
        rank_before = user.rank
        user.total_xp += xp_awarded
        if user.touch_streak(timezone.localdate()):
            events.append({"type": "streak", "label": f"{user.current_streak}-day streak", "xp": 0})

        level = challenge.level
        level_ids_needed = set(level.challenges.values_list("id", flat=True))
        if level_ids_needed and level_ids_needed <= solved_challenge_ids(user):
            _, created = LevelCompletion.objects.get_or_create(user=user, level=level)
            if created:
                level_completed = True
                user.total_xp += level.xp_reward
                xp_awarded += level.xp_reward
                events.append({"type": "level", "label": f"Level {level.index}: {level.title}", "xp": level.xp_reward})

                track = level.track
                track_level_ids = set(track.levels.values_list("id", flat=True))
                if track_level_ids <= completed_level_ids(user):
                    _, made = TrackCompletion.objects.get_or_create(user=user, track=track)
                    if made:
                        track_completed = True
                        events.append({"type": "track", "label": f"{track.name} complete", "xp": 0})

        user.save(update_fields=["total_xp", "current_streak", "longest_streak", "last_active_on"])
        if user.rank != rank_before:
            events.append({"type": "rank", "label": user.rank, "xp": 0})

        newly_open = [
            {"slug": t.slug, "name": t.name}
            for t in Track.objects.filter(required_xp__lte=user.total_xp, required_xp__gt=user.total_xp - xp_awarded)
        ]
        for t in newly_open:
            events.append({"type": "track_unlocked", "label": f"{t['name']} unlocked", "xp": 0})

    return {
        "correct": correct,
        "detail": detail,
        "xp_awarded": xp_awarded,
        "total_xp": user.total_xp,
        "rank": user.rank,
        "streak": user.current_streak,
        "already_solved": already_solved,
        "level_completed": level_completed,
        "track_completed": track_completed,
        "events": events,
    }
