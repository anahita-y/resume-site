from django import forms
from django.forms import inlineformset_factory
from .models import Skill,Interest , Resume, Education, Experience, Project, Award , Language


def fix_url(value):
    value = value.strip()
    if value and not value.startswith(("http://", "https://")):
        value = "https://" + value
    return value


class ResumeForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset = Skill.objects.all() ,
        widget = forms.CheckboxSelectMultiple ,
        required = False ,
        label = "مهارت‌ها" ,
    )

    interests = forms.ModelMultipleChoiceField(
        queryset = Interest.objects.all() ,
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = "به کدام حوزه‌ها علاقه دارید؟",
    )
    github = forms.CharField(label = "لینک گیت‌هاب" , required = False)
    linkedin = forms.CharField(label = "لینک لینکدین" , required = False)

    def clean_github(self):
        return fix_url(self.cleaned_data["github"])

    def clean_linkedin(self):
        return fix_url(self.cleaned_data["linkedin"])

    class Meta:
        model = Resume
        fields = [
            "first_name" , "last_name" , "email" , "phone" ,
            "github" , "linkedin" , "status" , "collaboration" ,
            "summary" , "skills" ,
        ]
        widgets = {"summary": forms.Textarea(attrs={"rows": 4})}


class ProjectForm(forms.ModelForm):
    link = forms.CharField(label = "لینک" , required = False)

    def clean_link(self):
        return fix_url(self.cleaned_data["link"])

    class Meta:
        model = Project
        fields = ["title" , "description" , "link"]


class AwardForm(forms.ModelForm):
    link = forms.CharField(label = "لینک مدرک یا گواهینامه" , required = False)

    def clean_link(self):
        return fix_url(self.cleaned_data["link"])

    class Meta:
        model = Award
        fields = ["title" , "issuer" , "date" , "link"]


EducationFormSet = inlineformset_factory(
    Resume ,
    Education ,
    fields = ["university" , "field" , "degree" , "start_year" , "end_year" , "gpa"] ,
    extra = 1 ,
    can_delete = False ,
)

ExperienceFormSet = inlineformset_factory(
    Resume ,
    Experience ,
    fields = ["title" , "organization" , "period" , "situation" , "task" , "action" , "result"] ,
    extra = 1 ,
    can_delete = False ,
)

ProjectFormSet = inlineformset_factory(
    Resume ,
    Project ,
    form = ProjectForm ,
    extra = 1 ,
    can_delete = False ,
)

AwardFormSet = inlineformset_factory(
    Resume ,
    Award ,
    form = AwardForm ,
    extra = 1 ,
    can_delete = False ,
)

LanguageFormSet = inlineformset_factory(
    Resume , 
    Language ,
    fields = ["name" , "level"] ,
    extra = 1 , 
    can_delete = False ,
)