from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from progress.services import build_state, completed_level_ids, level_is_unlocked, solved_challenge_ids

from .models import Level, Track
from .serializers import LevelDetailSerializer, TrackSerializer


class TrackListView(APIView):
    def get(self, request):
        return Response(build_state(request.user))


class TrackDetailView(APIView):
    def get(self, request, slug):
        state = build_state(request.user)
        for track in state:
            if track["slug"] == slug:
                return Response(track)
        return Response({"detail": "Not found."}, status=404)


class PublicTrackListView(APIView):
    """Unauthenticated preview for the landing page."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(TrackSerializer(Track.objects.all(), many=True).data)


class LevelDetailView(APIView):
    def get(self, request, pk):
        level = get_object_or_404(
            Level.objects.select_related("track").prefetch_related("lessons", "challenges"), pk=pk
        )
        track_unlocked = request.user.total_xp >= level.track.required_xp
        if not level_is_unlocked(level, completed_level_ids(request.user), track_unlocked):
            return Response(
                {"detail": "Locked. Finish the previous level first.", "locked": True}, status=403
            )
        data = LevelDetailSerializer(
            level, context={"solved_ids": solved_challenge_ids(request.user)}
        ).data
        return Response(data)
