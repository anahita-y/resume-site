from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.shortcuts import get_object_or_404 , redirect , render
from .forms import (
    ResumeForm , EducationFormSet , ExperienceFormSet ,
    ProjectFormSet , AwardFormSet , LanguageFormSet ,
)
from .models import Resume

def resume_create(request):
    resume = Resume()
    data = request.POST if request.method == "POST" else None

    form = ResumeForm(data , instance = resume)
    formsets = [
        ("تحصیلات", EducationFormSet(data, instance=resume)) ,
        ("تجربه‌ها", ExperienceFormSet(data, instance=resume)) ,
        ("پروژه‌ها", ProjectFormSet(data, instance=resume)) ,
        ("افتخارات و گواهینامه‌ها", AwardFormSet(data, instance=resume)) ,
        ("سطح زبان", LanguageFormSet(data, instance=resume)) ,
    ]

    if request.method == "POST":
        if form.is_valid() and all(fs.is_valid() for _, fs in formsets):
            with transaction.atomic():
                form.save()
                for _, fs in formsets:
                    fs.save()
            return redirect("resumes:success")
    return render(request , "resumes/form.html" , {"form" : form , "formsets" : formsets})

def success(request):
    return render(request , "resumes/success.html")



@staff_member_required
def resume_preview(request , pk):
    resume = get_object_or_404(Resume , pk = pk)
    return render(request , "resumes/resume_pdf.html", {"resume": resume})