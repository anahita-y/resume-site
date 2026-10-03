from django.db import transaction 
from django.shortcuts import render , redirect
from .forms import (ResumeForm , EducationFormSet , ExperienceFormSet,
                    ProjectFormSet , AwardFormSet ,)
from .models import Resume


def resume_create(request):
    resume = Resume()
    data = request.POST if request.method == "POST" else None

    form = ResumeForm(data , instance = resume)
    formsets = [
        ("تحصیلات", EducationFormSet(data, instance=resume)),
        ("تجربه‌ها", ExperienceFormSet(data, instance=resume)),
        ("پروژه‌ها", ProjectFormSet(data, instance=resume)),
        ("افتخارات و گواهینامه‌ها", AwardFormSet(data, instance=resume)),
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
