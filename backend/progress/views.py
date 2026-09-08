from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserSerializer
from curriculum.models import Challenge, Level

from .grading import grade
from .models import ChallengeAttempt, ChallengeSolve, LevelCompletion, TrackCompletion
from .services import build_state, completed_level_ids, level_is_unlocked, record_submission

User = get_user_model()


class SubmitView(APIView):
    throttle_scope = "submit"

    def post(self, request, pk):
        challenge = get_object_or_404(Challenge.objects.select_related("level__track"), pk=pk)
        level = challenge.level
        track_unlocked = request.user.total_xp >= level.track.required_xp
        if not level_is_unlocked(level, completed_level_ids(request.user), track_unlocked):
            return Response({"detail": "This level is locked."}, status=403)

        submission = request.data if isinstance(request.data, dict) else {}
        correct, detail = grade(challenge, submission)
        result = record_submission(request.user, challenge, submission, correct, detail)
        if correct:
            result["explanation"] = challenge.explanation
        return Response(result)


class DashboardView(APIView):
    def get(self, request):
        user = request.user
        state = build_state(user)
        solved = ChallengeSolve.objects.filter(user=user).count()
        total = Challenge.objects.count()
        attempts = ChallengeAttempt.objects.filter(user=user).count()

        # Where to pick back up: first unlocked, unfinished level.
        next_level = None
        for track in state:
            if not track["unlocked"]:
                continue
            for level in track["levels"]:
                if level["unlocked"] and not level["completed"]:
                    next_level = {
                        "id": level["id"],
                        "title": level["title"],
                        "index": level["index"],
                        "track_name": track["name"],
                        "track_slug": track["slug"],
                        "accent": track["accent"],
                    }
                    break
            if next_level:
                break

        recent = (
            ChallengeSolve.objects.filter(user=user)
            .select_related("challenge__level__track")
            .order_by("-solved_at")[:8]
        )
        return Response(
            {
                "user": UserSerializer(user).data,
                "tracks": state,
                "stats": {
                    "solved": solved,
                    "total_challenges": total,
                    "attempts": attempts,
                    "accuracy": round(100 * solved / attempts) if attempts else 0,
                    "levels_completed": len(completed_level_ids(user)),
                    "total_levels": Level.objects.count(),
                },
                "next_level": next_level,
                "recent_solves": [
                    {
                        "title": s.challenge.title,
                        "track": s.challenge.level.track.name,
                        "accent": s.challenge.level.track.accent,
                        "xp": s.challenge.xp,
                        "solved_at": s.solved_at,
                    }
                    for s in recent
                ],
            }
        )


class HistoryView(APIView):
    def get(self, request):
        user = request.user
        solves = (
            ChallengeSolve.objects.filter(user=user)
            .select_related("challenge__level__track")
            .order_by("-solved_at")
        )
        attempts = (
            ChallengeAttempt.objects.filter(user=user)
            .select_related("challenge__level__track")
            .order_by("-created_at")[:100]
        )

        vault = []
        seen_challenges = set()
        for att in attempts:
            if att.correct and att.challenge_id not in seen_challenges:
                seen_challenges.add(att.challenge_id)
                ch = att.challenge
                vault.append(
                    {
                        "challenge_id": ch.id,
                        "title": ch.title,
                        "kind": ch.kind,
                        "difficulty": ch.difficulty,
                        "xp": ch.xp,
                        "track_name": ch.level.track.name,
                        "track_slug": ch.level.track.slug,
                        "track_accent": ch.level.track.accent,
                        "level_index": ch.level.index,
                        "level_title": ch.level.title,
                        "submission": att.submission,
                        "solved_at": att.created_at,
                    }
                )

        return Response(
            {
                "vault": vault,
                "total_solved": solves.count(),
                "total_attempts": ChallengeAttempt.objects.filter(user=user).count(),
            }
        )


class ResetLevelView(APIView):
    def post(self, request, pk):
        user = request.user
        level = get_object_or_404(Level.objects.prefetch_related("challenges"), pk=pk)
        challenge_ids = list(level.challenges.values_list("id", flat=True))

        ChallengeSolve.objects.filter(user=user, challenge_id__in=challenge_ids).delete()
        ChallengeAttempt.objects.filter(user=user, challenge_id__in=challenge_ids).delete()
        LevelCompletion.objects.filter(user=user, level=level).delete()

        return Response({"success": True, "detail": f"Level {level.index} reset successfully."})
