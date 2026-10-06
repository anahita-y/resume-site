from django.db import models
import uuid
class Skill(models.Model):
    name = models.CharField("مهارت" , max_length = 50 , unique = True)

    class Meta:
        verbose_name = "مهارت"
        verbose_name_plural = "مهارت ها"

    def __str__(self):
        return  self.name

class Interest(models.Model):
    name = models.CharField("حوزه" , max_length = 50 , unique = True)


    class Meta:
        verbose_name = "حوزه‌ی علاقه"
        verbose_name_plural = "حوزه‌های علاقه"

    def __str__(self):
        return self.name


class Resume(models.Model):
    first_name = models.CharField("نام" , max_length = 50)
    last_name = models.CharField("نام خانوادگی" , max_length = 50)
    email = models.EmailField("ایمیل")
    phone = models.CharField("شماره تماس" , max_length = 20)
    github = models.URLField("لینک گیت‌هاب" , blank = True)
    linkedin = models.URLField("لینک لینکدین" , blank = True)
    summary = models.TextField("درباره من (خلاصه)" , blank = True)
    STATUS_CHOIES = [
        ("student", "دانشجوی فعلی"),
        ("graduate_collab", "فارغ‌التحصیل و همکار دانشگاه"),
        ("graduate", "فارغ‌التحصیل"),
    ]
    status = models.CharField("وضعیت" , max_length = 20 , choices = STATUS_CHOIES , default = "student")
    collaboration = models.CharField("نوع همکاری با دانشگاه (مثلاً عضو انجمن، دستیار آموزشی، پژوهشگر)" , max_length = 150 , blank = True)
    skills = models.ManyToManyField(Skill , verbose_name = "مهارت‌ها" , blank = True)
    other_skills = models.CharField("مهارت‌های دیگر" , max_length = 1000 , blank = True)
    interests = models.ManyToManyField(Interest , verbose_name = "حوزه‌های مورد علاقه" , blank = True)
    created_at = models.DateField("تاریخ ثبت" , auto_now_add = True)
    token = models.UUIDField(default = uuid.uuid4 ,editable = False , db_index = True)
    pdf = models.FileField("فایل PDF" ,  upload_to = "resume_pdfs/" , blank = True)
    class Meta:
        verbose_name = "رزومه"
        verbose_name_plural = "رزومه ها"
        ordering = ["-created_at"]


    def __set__(self):
        return f"{self.first_name} {self.last_name}"



class Education(models.Model):
    DEGREES = [
        ("associate" , "کاردانی"),
        ("bachelor" , "کارشناسی"),
        ("master" , "کارشناسی ارشد"),
        ("phd" , "دکتری"),
    ]

    resume = models.ForeignKey(Resume , on_delete = models.CASCADE , related_name = "educations")
    university = models.CharField("دانشگاه" , max_length = 100)
    field = models.CharField("رشته" , max_length = 100)
    degree = models.CharField("مقطع" , max_length = 20 , choices = DEGREES)
    start_year = models.CharField("سال ورود" , max_length = 10)
    end_year = models.CharField("سال پایان (خالی = در حال تحصیل)" , max_length = 10 , blank = True)
    gpa = models.CharField("معدل" , max_length = 10 , blank = True)

    class Meta:
        verbose_name = "تحصیلات" 
        verbose_name_plural = "تحصیلات"


class Experience(models.Model):
    resume = models.ForeignKey(Resume , on_delete = models.CASCADE , related_name = "experiences")
    title = models.CharField("عنوان" , max_length = 100)
    organization = models.CharField("سازمان یا مجموعه" , max_length = 100 ,blank = True)
    period = models.CharField("بازه‌ی زمانی" , max_length = 50 , blank = True)
    situation = models.TextField("موقعیت" , blank = True)
    task = models.TextField("وظیفه" , blank = True)
    action = models.TextField("اقدام" , blank = True)
    result = models.TextField("نتیجه" , blank = True)

    class Meta:
        verbose_name = "تجربه"
        verbose_name_plural = "تجربه‌ها"


class Project(models.Model):
    resume = models.ForeignKey(Resume , on_delete = models.CASCADE , related_name = "projects")
    title = models.CharField("عنوان پروژه" , max_length = 100)
    description = models.TextField("توضیح کوتاه" , blank = True)
    link = models.URLField("لینک" , blank = True)

    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"


class Award(models.Model):
    resume = models.ForeignKey(Resume , on_delete = models.CASCADE , related_name = "awards")
    title = models.CharField("عنوان" , max_length = 100)
    issuer = models.CharField("نهاد صادرکننده" , max_length = 100 , blank = True)
    date = models.CharField("تاریخ" ,  max_length = 30 , blank = True)
    link = models.URLField("لینک مدرک یا گواهینامه" , blank = True)
    
    class Meta:
        verbose_name = "افتخار یا گواهینامه"
        verbose_name_plural = "افتخارات و گواهینامه‌ها"



class Language(models.Model):
    LEVELS = [
        ("basic", "مقدماتی"),
        ("intermediate", "متوسط"),
        ("advanced", "پیشرفته"),
        ("fluent", "مسلط"),
        ("native", "زبان مادری"),
    ]
    resume = models.ForeignKey(Resume , on_delete = models.CASCADE , related_name = "languages")
    name = models.CharField("زبان" , max_length = 50)
    level = models.CharField("سطح" , max_length = 20 , choices = LEVELS)

    class Meta:
        verbose_name = "زبان"
        verbose_name_plural = "زبان‌ها"

        