from django.urls import path
from .views import (
    get_jobs,
    get_job_details,
    apply_job,
    get_applied_jobs,
    delete_application,
    company_login,
    add_job,
    get_company_jobs,
    delete_job,
    job_applicants,
    company_register,
    get_job_applicants,
    
)

urlpatterns = [
    
    path("",get_jobs),  # /api/jobs/
    path("<int:id>/", get_job_details),  # /api/jobs/1/
    path("apply/", apply_job),
    path("applications/", get_applied_jobs),

    # DELETE
    path("applications/delete/<int:id>/", delete_application),
    path("company/login/",company_login),
    path("add/",add_job),
    path("company/jobs/<int:company_id>/",get_company_jobs),
    path("delete/<int:id>/",delete_job),
    path("applicants/int:job_id>/",job_applicants),
    path("company/register/",company_register),
    path("applicant/<int:job_id>/",get_job_applicants),
]