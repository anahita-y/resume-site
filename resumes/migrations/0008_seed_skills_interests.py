from django.db import migrations

SKILLS = [
    "Python", "Django", "Django REST Framework", "FastAPI", "Flask",
    "JavaScript", "TypeScript", "React", "Node.js", "HTML/CSS",
    "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis",
    "Git/GitHub", "Docker", "Linux", "REST API",
    "C", "C++", "C#", "Java", "Kotlin", "Flutter",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "Pandas/NumPy", "PyTorch", "TensorFlow", "Data Analysis", "Power BI",
    "Arduino/ESP32", "Raspberry Pi", "Computer Networks", "Cybersecurity",
    "UI/UX Design", "Figma",
]
INTERESTS = [
    "بک‌اند", "فرانت‌اند", "هوش مصنوعی", "علم داده", "امنیت", "موبایل",
    "شبکه", "اینترنت اشیا", "دواپس", "بازی‌سازی", "طراحی UI/UX",
]


def seed(apps, schema_editor):
    Skill = apps.get_model("resumes", "Skill")
    Interest = apps.get_model("resumes", "Interest")
    for name in SKILLS:
        Skill.objects.get_or_create(name=name)
    for name in INTERESTS:
        Interest.objects.get_or_create(name=name)


class Migration(migrations.Migration):
    dependencies = [("resumes", "0007_resume_other_skills")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]