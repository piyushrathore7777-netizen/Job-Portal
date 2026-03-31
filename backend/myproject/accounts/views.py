from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from jobs.models import Company
from jobs.models import Job

# REGISTER
@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"})

    User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({"message": "User registered successfully"})


# LOGIN
@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        return Response({
            "message": "Login successful",
            "username": user.username,
            "email": user.email
        })
    else:
        return Response({"error": "Invalid credentials"})


# COMPANY REGISTER
@api_view(['POST'])
def company_register(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')

    if Company.objects.filter(email=email).exists():
        return Response({"error": "Company already exists"})

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

@api_view(['POST'])
def company_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        company = Company.objects.get(email=email, password=password)
        return Response({
            "message": "Login success",
            "company": {
                "id": company.id,
                "name": company.name,
                "email": company.email
            }
        })
    except Company.DoesNotExist:
        return Response({"error": "Invalid credentials"})


@api_view(['POST'])
def post_job(request):
    company_id = request.data.get('company_id')
    title = request.data.get('title')
    description = request.data.get('description')
    salary = request.data.get('salary')

    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"})

    job = Job.objects.create(
        company=company,
        title=title,
        description=description,
        salary=salary
    )

    return Response({"message": "Job posted successfully"})