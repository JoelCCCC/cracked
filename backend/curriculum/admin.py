from django.contrib import admin

from .models import Challenge, Lesson, Level, Track


class LevelInline(admin.TabularInline):
    model = Level
    extra = 0


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "required_xp")
    inlines = [LevelInline]


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0


class ChallengeInline(admin.StackedInline):
    model = Challenge
    extra = 0


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("__str__", "track", "index", "xp_reward")
    list_filter = ("track",)
    inlines = [LessonInline, ChallengeInline]


admin.site.register(Lesson)
admin.site.register(Challenge)
