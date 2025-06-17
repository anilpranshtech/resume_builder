from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import Resume, Education, Experience, Skill, Project

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'myproject/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('resume_list')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'myproject/login.html')

@login_required
def select_theme(request):
    if request.method == 'POST':
        form = ThemeSelectionForm(request.POST)
        if form.is_valid():
            selected_theme = form.cleaned_data['theme']
            request.session['selected_theme'] = selected_theme 
            return redirect('create_resume')
    else:
        form = ThemeSelectionForm()
    return render(request, 'myproject/theme_selection.html', {'form': form})

@login_required
def create_resume(request):
    selected_theme = request.session.get('selected_theme', 'modern') 

    if request.method == 'POST':
        resume_form = ResumeForm(request.POST, request.FILES)
        education_form = EducationForm(request.POST)
        experience_form = ExperienceForm(request.POST)
        skill_form = SkillForm(request.POST)
        project_form = ProjectForm(request.POST)

        if all([resume_form.is_valid(), education_form.is_valid(), experience_form.is_valid(), skill_form.is_valid(), project_form.is_valid()]):
            resume = resume_form.save(commit=False)
            resume.user = request.user
            resume.theme = selected_theme 
            resume.save()

            if 'selected_theme' in request.session:
                del request.session['selected_theme']
            for form_instance in [education_form, experience_form, skill_form, project_form]:
                instance = form_instance.save(commit=False)
                instance.resume = resume
                instance.save()

            return redirect('resume_list')
    else:
        resume_form = ResumeForm()
        education_form = EducationForm()
        experience_form = ExperienceForm()
        skill_form = SkillForm()
        project_form = ProjectForm()

    return render(request, 'myproject/resume_form.html', {
        'resume_form': resume_form,
        'education_form': education_form,
        'experience_form': experience_form,
        'skill_form': skill_form,
        'project_form': project_form,
        'is_edit': False,
        'selected_theme': selected_theme,
    })

@login_required
def edit_resume(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)

    if request.method == 'POST':
        resume_form = ResumeForm(request.POST, request.FILES, instance=resume)
        education_instance = resume.education_set.first()
        experience_instance = resume.experience_set.first()
        skill_instance = resume.skill_set.first()
        project_instance = resume.project_set.first()

        education_form = EducationForm(request.POST, instance=education_instance)
        experience_form = ExperienceForm(request.POST, instance=experience_instance)
        skill_form = SkillForm(request.POST, instance=skill_instance)
        project_form = ProjectForm(request.POST, instance=project_instance)

        if all([resume_form.is_valid(), education_form.is_valid(), experience_form.is_valid(), skill_form.is_valid(), project_form.is_valid()]):
            resume_form.save()
            for form_instance, model_class in [
                (education_form, Education),
                (experience_form, Experience),
                (skill_form, Skill),
                (project_form, Project)
            ]:
                if form_instance.instance.pk:
                    form_instance.save()
                else: 
                    instance = form_instance.save(commit=False)
                    instance.resume = resume
                    instance.save()

            return redirect('resume_list')
    else:
        resume_form = ResumeForm(instance=resume)
        education_form = EducationForm(instance=resume.education_set.first())
        experience_form = ExperienceForm(instance=resume.experience_set.first())
        skill_form = SkillForm(instance=resume.skill_set.first())
        project_form = ProjectForm(instance=resume.project_set.first())

    return render(request, 'myproject/resume_form.html', {
        'resume_form': resume_form,
        'education_form': education_form,
        'experience_form': experience_form,
        'skill_form': skill_form,
        'project_form': project_form,
        'is_edit': True,
        'selected_theme': resume.theme, 
    })

@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'myproject/resume_list.html', {'resumes': resumes})

@login_required
def resume_detail(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    return render(request, 'myproject/resume_detail.html', {'resume': resume})

@login_required
def resume_delete(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    resume.delete()
    return redirect('resume_list')