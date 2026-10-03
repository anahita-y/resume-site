from django import forms
from django.forms import inlineformset_factory
from .models import Skill, Resume, Education, Experience, Project, Award


class ResumeForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset = Skill.objects.all() ,
        widget = forms.CheckboxSelectMultiple ,
        required = False ,
        label = "مهارت‌ها" ,
    )

    class Meta:
        model = Resume
        fields = [
            "first_name" , "last_name" , "email" , "phone" ,
            "github" , "linkedin" , "status" , "collaboration" ,
            "summary" , "skills" ,
        ]
        widgets = {"summary": forms.Textarea(attrs={"rows": 4})}


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
    fields = ["title" , "description" , "link"] ,
    extra = 1 , 
    can_delete = False ,
)

AwardFormSet = inlineformset_factory(
    Resume , 
    Award ,
    fields = ["title" , "issuer" , "date" , "link"] ,
    extra= 1 , 
    can_delete = False,
)