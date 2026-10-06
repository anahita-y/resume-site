from resumes.models import Skill, Interest

skills = [
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
interests = [
    "بک‌اند", "فرانت‌اند", "هوش مصنوعی", "علم داده", "امنیت", "موبایل",
    "شبکه", "اینترنت اشیا", "دواپس", "بازی‌سازی", "طراحی UI/UX",
]

for n in skills:
    Skill.objects.get_or_create(name=n)
for n in interests:
    Interest.objects.get_or_create(name=n)
print("done")