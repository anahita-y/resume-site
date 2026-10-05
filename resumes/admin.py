from django.contrib import admin
from .models import (Skill , Interest ,  Resume , 
    Education , Experience , Project , Award , Language)


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

class LanguageInline(admin.TabularInline):
    model = Language
    extra = 0


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "status", "created_at")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("status", "skills" , "interests")
    filter_horizontal = ("skills", "interests")
    inlines = [EducationInline,  ExperienceInline, ProjectInline, AwardInline , LanguageInline]



admin.site.register(Skill)
admin.site.register(Interest)

