from django.db import migrations

WORK_CONDITIONS = ["حضوری" , "دورکاری" , "ترکیبی" , "پاره‌وقت" , "تمام‌وقت"]


def seed(apps , schema_editor):
    WorkCondition = apps.get_model("resumes" , "WorkCondition")
    for name in WORK_CONDITIONS:
        WorkCondition.objects.get_or_create(name = name)


class Migration(migrations.Migration):

    dependencies = [
        ("resumes", "0010_workcondition_remove_resume_work_conditions_and_more"),
    ]

    operations = [
        migrations.RunPython(seed , migrations.RunPython.noop) ,
    ]