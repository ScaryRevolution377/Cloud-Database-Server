import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from supabase import create_client, Client
from .models import UserFile


def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    return create_client(url,key)

@login_required
def dashboard(request):
    supabase = get_supabase_client()
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        file_path = f"{request.user.id}/{uploaded_file.name}"

        supabase.storage.from_("user-files").upload(
            file_path,
            uploaded_file.read(),
            file_options={"content-type": uploaded_file.content_type}
        )

        file_url = supabase.storage.from_("user-files").get_public_url(file_path)

        UserFile.objects.create(
            user=request.user,
            file_name=uploaded_file.name,
            file_url=file_url
        )

        return redirect ("dashboard")

    files = request.user.files.all().order_by("-uploaded_at")
    return render(request, "core/dashboard.html", {"files": files})

@login_required
def delete_file(request, file_id):
    file_obj = get_object_or_404(UserFile, id=file_id, user=request.user)

    supabase = get_supabase_client()

    file_path = f"{request.user.id}/{file_obj.file_name}"
    supabase.storage.from_("user-files").remove([file_path])

    file_obj.delete()
    return redirect("dashboard")





