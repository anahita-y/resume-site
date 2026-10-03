from django.contrib import admin
from .models import Skill , Resume , Education , Experience , Project , Award


class EducationInline(admin.StackedInline):
    model = Education
    extra = 0


class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 0


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0


class AwardInline(admin.StackedInline):
    model = Award
    extra = 0


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "status", "created_at")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("status", "skills")
    inlines = [EducationInline, ExperienceInline, ProjectInline, AwardInline]


admin.site.register(Skill)
