from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    class GenderStatus(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_info"
    )

    name = models.CharField(max_length=40)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GenderStatus.choices)
    email = models.EmailField(max_length=40, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)


class Address(models.Model):
    class Type(models.TextChoices):
        PRESENT = "present", "Present"
        PERMANENT = "permanent", "Permanent"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address")
    type = models.CharField(max_length=10, choices=Type.choices)

    address = models.CharField(max_length=125)
    post_name = models.CharField(max_length=125, blank=True, null=True)
    post_code = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.village



class BaseEducation(models.Model):
    institute = models.CharField(max_length=120)
    passing_year = models.CharField(max_length=4, blank=True, null=True)
    result = models.CharField(max_length=127, blank=True, null=True)


    class Meta:
        abstract = True


class AcademicEducation(BaseEducation):
    class LevelStatus(models.TextChoices):
        JSC = "jsc", "JSC"
        SSC = "ssc", "SSC"
        HSC = "hsc", "HSC"
        O_LEVEL = "o_level", "O-LEVEL"
        A_LEVEL = "a_level", "A-LEVEL"
        BSC = "bachelors", "BACHELORS"
        MSC = "masters", "MASTERS"
        PHD = "phd", "PHD"
        DIPLOMA = "diploma", "DIPLOMA"
        CA_QUALIFIED = "ca_qualified", "CA QUALIFIED"
        CA_CC = "ca_cc", "CA CC"
        CMA_QUALIFIED = "cma_qualified", "CMA QUALIFIED"
        CMA_STUDENT = "cma_student", "CMA STUDENT"
        ACCA = "acca", "ACCA"
        CS = "cs", "CS"
        MBBS = "mbbs", "MBBS"
        BDS = "bds", "BDS"
        LLB = "llb", "LLB"
        LLM = "llm", "LLM"
        OTHER = "other", "OTHER"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="academic_education"
    )
    levels = models.CharField(max_length=20, choices=LevelStatus.choices)
    subject = models.CharField(max_length=120)
    board = models.CharField(max_length=120)



class Employed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employed")

    company_name = models.CharField(max_length=120)
    company_type = models.CharField(max_length=120, blank=True, null=True)
    position = models.CharField(max_length=120)
    joining_date = models.DateField(null=True, blank=True)
    leaving_date = models.DateField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    responsibility = models.TextField(blank=True, null=True)


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=50)




