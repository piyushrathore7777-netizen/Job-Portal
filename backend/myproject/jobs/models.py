from django.db import models

# ✅ Company Model (only ONE)
class Company(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name


# ✅ Job Model (only ONE)
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    salary = models.IntegerField()
    apply_link = models.URLField(blank=True, null=True)  # 🔥 ADD ONLY THIS    

    def __str__(self):
        return self.title


# ✅ Apply Model
class Apply(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.name

       