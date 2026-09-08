from django.core.management.base import BaseCommand
from django.db import transaction

from curriculum.content import ai, algorithms, coding, databases, devops, webdev
from curriculum.models import Challenge, Lesson, Level, Track

TRACKS = [coding.TRACK, algorithms.TRACK, webdev.TRACK, databases.TRACK, devops.TRACK, ai.TRACK]


class Command(BaseCommand):
    help = "Create or update the curriculum from curriculum/content/*.py. Idempotent."

    def add_arguments(self, parser):
        parser.add_argument(
            "--prune",
            action="store_true",
            help="Delete levels/lessons/challenges that are no longer in the content files.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        prune = options["prune"]
        counts = {"tracks": 0, "levels": 0, "lessons": 0, "challenges": 0}

        for spec in TRACKS:
            levels = spec.pop("levels")
            track, _ = Track.objects.update_or_create(slug=spec["slug"], defaults=spec)
            spec["levels"] = levels
            counts["tracks"] += 1

            seen_levels = []
            for level_spec in levels:
                lessons = level_spec.pop("lessons", [])
                challenges = level_spec.pop("challenges", [])
                level, _ = Level.objects.update_or_create(
                    track=track,
                    index=level_spec["index"],
                    defaults={k: v for k, v in level_spec.items() if k != "index"},
                )
                level_spec["lessons"] = lessons
                level_spec["challenges"] = challenges
                seen_levels.append(level.id)
                counts["levels"] += 1

                seen_lessons = []
                for order, lesson_spec in enumerate(lessons):
                    lesson, _ = Lesson.objects.update_or_create(
                        level=level,
                        order=order,
                        defaults={k: v for k, v in lesson_spec.items()},
                    )
                    seen_lessons.append(lesson.id)
                    counts["lessons"] += 1

                seen_challenges = []
                for order, ch_spec in enumerate(challenges):
                    challenge, _ = Challenge.objects.update_or_create(
                        level=level,
                        order=order,
                        defaults={k: v for k, v in ch_spec.items()},
                    )
                    seen_challenges.append(challenge.id)
                    counts["challenges"] += 1

                if prune:
                    level.lessons.exclude(id__in=seen_lessons).delete()
                    level.challenges.exclude(id__in=seen_challenges).delete()

            if prune:
                track.levels.exclude(id__in=seen_levels).delete()

        if prune:
            Track.objects.exclude(slug__in=[t["slug"] for t in TRACKS]).delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded {tracks} tracks, {levels} levels, {lessons} lessons, {challenges} challenges.".format(**counts)
            )
        )
