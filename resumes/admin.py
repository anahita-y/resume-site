from django.contrib import admin , messages
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import Truncator
from .latex import build_resume_pdf
from .models import (Skill , Interest , WorkCondition ,  Resume , 
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
    list_display = (
        "first_name" , "last_name" , "status" ,
        "degree_col" , "field_col" , "entry_year_col" ,
        "skills_col" , "other_skills_col" , "interests_col" ,
        "work_types_col" , pdf_link , "created_at" ,
    )
    search_fields = (
        "first_name" , "last_name" , "email" ,
        "other_skills" , "future_plan" ,
        "educations__field" , "educations__university" ,
    )
    list_filter = (
        "status" , "skills" , "interests" , "work_types" ,
        "educations__degree" , "educations__field" , "educations__start_year" ,
    )
    filter_horizontal = ("skills" , "interests" , "work_types")
    inlines = [EducationInline,  ExperienceInline, ProjectInline, AwardInline , LanguageInline]
    actions = [rebuild_pdf]

    def get_queryset(self , request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("skills" , "interests" , "work_types" , "educations")

    @admin.display(description = "مقطع")
    def degree_col(self , obj):
        return "، ".join(e.get_degree_display() for e in obj.educations.all()) or "-"

    @admin.display(description = "رشته")
    def field_col(self , obj):
        return "، ".join(e.field for e in obj.educations.all()) or "-"

    @admin.display(description = "سال ورود")
    def entry_year_col(self , obj):
        return "، ".join(e.start_year for e in obj.educations.all()) or "-"

    @admin.display(description = "مهارت‌های لیست")
    def skills_col(self , obj):
        text = "، ".join(s.name for s in obj.skills.all())
        return Truncator(text).chars(60) if text else "-"

    @admin.display(description = "مهارت‌های خارج از لیست")
    def other_skills_col(self , obj):
        return Truncator(obj.other_skills).chars(60) if obj.other_skills else "-"

    @admin.display(description = "حوزه‌های علاقه")
    def interests_col(self , obj):
        text = "، ".join(i.name for i in obj.interests.all())
        return Truncator(text).chars(60) if text else "-"

    @admin.display(description = "شرایط کاری")
    def work_types_col(self , obj):
        return "، ".join(w.name for w in obj.work_types.all()) or "-"


admin.site.register(Skill)
admin.site.register(Interest)
admin.site.register(WorkCondition)