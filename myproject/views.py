from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  *

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  
    else:
        form = RegisterForm()
    return render(request, 'myproject/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create_resume')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'myproject/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def create_resume_view(request):
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST)
        education_form = EducationForm(request.POST)
        experience_form = ExperienceForm(request.POST)
        skill_form = SkillForm(request.POST)
        project_form = ProjectForm(request.POST)

        forms = [resume_form, education_form, experience_form, skill_form, project_form]

        if all(form.is_valid() for form in forms):
            resume = resume_form.save(commit=False)
            resume.user = request.user
            resume.save()

            for form in [education_form, experience_form, skill_form, project_form]:
                obj = form.save(commit=False)
                obj.resume = resume
                obj.save()

            return redirect('create_resume')
    else:
        resume_form = ResumeForm()
        education_form = EducationForm()
        experience_form = ExperienceForm()
        skill_form = SkillForm()
        project_form = ProjectForm()

    context = {
        'resume_form': resume_form,
        'education_form': education_form,
        'experience_form': experience_form,
        'skill_form': skill_form,
        'project_form': project_form
    }
    return render(request, 'myproject/resume_form.html', context)
