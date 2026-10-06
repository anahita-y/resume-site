import logging
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import FileResponse , Http404
from django.shortcuts import get_object_or_404 , redirect , render
from .forms import (
    ResumeForm , EducationFormSet , ExperienceFormSet ,
    ProjectFormSet , AwardFormSet , LanguageFormSet ,
)
from .latex import build_resume_pdf
from .models import Resume

logger = logging.getLogger(__name__)


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
                resume = form.save()
                for _, fs in formsets:
                    fs.save()
            try:
                build_resume_pdf(resume)
            except Exception:
                logger.exception("PDF build failed for resume %s", resume.pk)
            return redirect("resumes:success", token=resume.token)

    return render(request, "resumes/form.html", {"form": form, "formsets": formsets})


def success(request , token):
    resume = get_object_or_404(Resume , token = token)
    return render(request , "resumes/success.html" , {"resume"  : resume})


def download(request, token):
    resume = get_object_or_404(Resume, token=token)
    if not resume.pdf:
        raise Http404("PDF not ready")
    return FileResponse(
        resume.pdf.open("rb") ,
        as_attachment=True ,
        filename=f"resume_{resume.pk}.pdf" ,
        content_type="application/pdf" ,
    )



@staff_member_required
def resume_preview(request , pk):
    resume = get_object_or_404(Resume , pk = pk)
    return render(request , "resumes/resume_pdf.html", {"resume": resume})