from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Job, Apply
from .serializers import JobSerializer
from .models import Company
import requests



# Home
def home(request):
    return HttpResponse("Welcome to Job Portal")


# GET all jobs
@api_view(['GET'])
def get_jobs(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


# GET single job ( FIXED)
@api_view(['GET'])
def get_job_details(request, id):
    try:
        job = Job.objects.get(id=id)
        serializer = JobSerializer(job)
        return Response(serializer.data)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)


# APPLY JOB
@api_view(['POST'])
def apply_job(request):
    data = request.data

    name = data.get('name')
    email = data.get('email')
    job_id = data.get('job')
    resume = request.FILES.get('resume')

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    # already applied check
    if Apply.objects.filter(email=email, job=job).exists():
        return Response({"message": "Already applied"})

    Apply.objects.create(
        name=name,
        email=email,
        job=job,
        resume=resume,
    )

    return Response({"message": "Applied successfully with resume"})


# GET applied jobs
@api_view(['GET'])
def get_applied_jobs(request):
    email = request.GET.get('email')

    applications = Apply.objects.filter(email=email)

    data = []
    for app in applications:
        data.append({
            "id": app.id,
            "name": app.name,
            "email": app.email,
            "job_title": app.job.title,
        })

    return Response(data)


# DELETE application
@api_view(['DELETE'])
def delete_application(request, id):
    try:
        app = Apply.objects.get(id=id)
        app.delete()
        return Response({"message": "Deleted successfully"})
    except Apply.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


@api_view(['POST'])
def company_login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        company = Company.objects.get(email=email, password=password)

        return Response({
            "message": "Login successful ",
            "company": {
                "id": company.id,
                "name": company.name,
                "email": company.email
            }
        })

    except Company.DoesNotExist:
        return Response({"error": "Invalid email or password "}, status=400)


@api_view(['POST'])
def add_job(request):
    data = request.data

    title = data.get("title")
    description = data.get("description")
    salary = data.get("salary")
    category = data.get("category",)
    company_id = data.get("company")

    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=404)

    Job.objects.create(
        title=title,
        description=description,
        salary=salary,
        category=category,
        company=company
    )

    return Response({"message": "Job posted successfully"})


@api_view(['GET'])
def get_company_jobs(request, company_id):
    jobs = Job.objects.filter(company_id=company_id)

    data = []
    for job in jobs:
        data.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "salary": job.salary,
        })

    return Response(data)


@api_view(['DELETE'])
def delete_job(request, id):
    try:
        job = Job.objects.get(id=id)
        job.delete()
        return Response({"message": "Job deleted successfully"})
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)


@api_view(['GET'])
def job_applicants(request, job_id):
    applications = Apply.objects.filter(job_id=job_id)

    data = []
    for app in applications:
        data.append({
            "id": app.id,
            "name": app.name,
            "email": app.email
        })

    return Response(data)


@api_view(['POST'])
def company_register(request):
    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")

    # check if already exists
    if Company.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=400)

    company = Company.objects.create(
        name=name,
        email=email,
        password=password
    )

    return Response({
        "message": "Company registered successfully",
        "company": {
            "id": company.id,
            "name": company.name,
            "email": company.email
        }
    })

    from .models import Apply

@api_view(['GET'])
def get_job_applicants(request, job_id):
    applications = Apply.objects.filter(job_id=job_id)

    data = []
    for app in applications:
        data.append({
            "id": app.id,
            "name": app.name,
            "email": app.email,
            "resume": app.resume.url if app.resume else None
        })

    return Response(data)



@api_view(['GET'])
def external_jobs(request):
    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": "developer jobs in india",
        "page": "1"
    }

    headers = {
        "X-RapidAPI-Key": "cfe9cfbfb3mshf31085d505cf35cp1ac74bjsn1ba4da816651",
        "X-RapidAPI-Host": "linkedin-job-search-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    jobs = []

    for job in data.get("data", []):
        jobs.append({
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "salary": job.get("job_salary"),
            "apply_link": job.get("job_apply_link"),
        })

    return Response(jobs)