from rest_framework import serializers

from .models import Challenge, Lesson, Level, Track


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "order", "title", "body", "minutes")


class ChallengeSerializer(serializers.ModelSerializer):
    """Public view of a challenge. `solution` is deliberately excluded."""

    solved = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = (
            "id",
            "order",
            "kind",
            "difficulty",
            "title",
            "prompt",
            "hint",
            "xp",
            "config",
            "solved",
        )

    def get_solved(self, obj):
        return obj.id in self.context.get("solved_ids", set())


class LevelDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    challenges = ChallengeSerializer(many=True, read_only=True)
    track = serializers.SerializerMethodField()
    next_level_id = serializers.SerializerMethodField()

    class Meta:
        model = Level
        fields = (
            "id",
            "index",
            "title",
            "summary",
            "xp_reward",
            "track",
            "lessons",
            "challenges",
            "next_level_id",
        )

    def get_track(self, obj):
        return {
            "slug": obj.track.slug,
            "name": obj.track.name,
            "accent": obj.track.accent,
            "icon": obj.track.icon,
        }

    def get_next_level_id(self, obj):
        nxt = Level.objects.filter(track_id=obj.track_id, index=obj.index + 1).first()
        return nxt.id if nxt else None


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ("id", "slug", "name", "tagline", "description", "icon", "accent", "order", "required_xp")
