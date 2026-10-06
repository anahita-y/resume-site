from django.contrib import admin , messages
from django.urls import reverse
from django.utils.html import format_html
from .latex import build_resume_pdf
from .models import (Skill , Interest ,  Resume , 
    Education , Experience , Project , Award , 
    Language)

@admin.display(description = "PDF")
def pdf_link(obj):
    if obj.pdf:
        url = reverse("resumes:download" , args = [obj.token])
        return format_html('<a href="{}">دانلود PDF</a>' ,url)
    return "-"

@admin.action(description = "ساخت دوباره‌ی PDF برای رزومه‌های انتخاب‌شده")
def rebuild_pdf(modeladmin , request , queryset):
    done = 0
    for resume in queryset:
        try:
            build_resume_pdf(resume)
            done +=1
        except Exception as exc:
            modeladmin.message_user(request , f"{resume} : {exc}" , level =messages.ERROR)
        if done:
            modeladmin.message_user(request , f"{done} فایل PDF ساخته شد.")

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
    list_display = ("first_name", "last_name", "email", "status", pdf_link , "created_at")
    search_fields = ("first_name", "last_name", "email" , "other_skills")
    list_filter = ("status", "skills" , "interests")
    filter_horizontal = ("skills", "interests")
    inlines = [EducationInline,  ExperienceInline, ProjectInline, AwardInline , LanguageInline]
    actions = [rebuild_pdf]


admin.site.register(Skill)
admin.site.register(Interest)


