from django.db import models


class Track(models.Model):
    """A discipline: coding, algorithms, web, db, devops, ai."""

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=80)
    tagline = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=8, default="*")
    accent = models.CharField(max_length=20, default="#7c5cff")
    order = models.PositiveIntegerField(default=0)
    # XP the learner must hold before this track opens. Keeps the path linear
    # without hard-blocking someone who grinds an earlier track.
    required_xp = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return self.name


class Level(models.Model):
    track = models.ForeignKey(Track, related_name="levels", on_delete=models.CASCADE)
    index = models.PositiveIntegerField(help_text="1-based position inside the track")
    title = models.CharField(max_length=120)
    summary = models.TextField(blank=True)
    xp_reward = models.PositiveIntegerField(default=50, help_text="Bonus XP for clearing the level")

    class Meta:
        ordering = ("track__order", "index")
        unique_together = ("track", "index")

    def __str__(self):
        return f"{self.track.slug} L{self.index}: {self.title}"


class Lesson(models.Model):
    level = models.ForeignKey(Level, related_name="lessons", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=140)
    body = models.TextField(help_text="Markdown")
    minutes = models.PositiveIntegerField(default=5)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return self.title


class Challenge(models.Model):
    class Kind(models.TextChoices):
        MCQ = "mcq", "Multiple choice"
        MULTI = "multi", "Multiple answers"
        SHORT = "short", "Short answer"
        CODE = "code", "Code"

    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    level = models.ForeignKey(Level, related_name="challenges", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    kind = models.CharField(max_length=10, choices=Kind.choices)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY)
    title = models.CharField(max_length=160)
    prompt = models.TextField(help_text="Markdown")
    hint = models.TextField(blank=True)
    explanation = models.TextField(blank=True, help_text="Shown after a correct answer")
    xp = models.PositiveIntegerField(default=20)

    # Public shape, safe to send to the browser.
    #   mcq/multi -> {"options": ["a", "b", ...]}
    #   short     -> {"placeholder": "..."}
    #   code      -> {"language": "python", "starter": "...", "signature": "def f(x):"}
    config = models.JSONField(default=dict, blank=True)

    # Never serialized to the client.
    #   mcq       -> {"answer": 2}
    #   multi     -> {"answers": [0, 3]}
    #   short     -> {"accept": ["regex1", ...], "ignore_case": true}
    #   code      -> {"entrypoint": "solve", "cases": [{"args": [1], "expect": 2}]}
    solution = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return self.title
