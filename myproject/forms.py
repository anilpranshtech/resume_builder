from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Resume, Education, Experience, Skill, Project, User # Import User model

# Your existing forms
class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class ThemeSelectionForm(forms.Form):
    theme = forms.ChoiceField(choices=Resume.THEME_CHOICES, widget=forms.RadioSelect)

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        # Add 'profile_picture' to the fields
        fields = ['full_name', 'email', 'phone', 'location', 'summary', 'profile_picture']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'start_year', 'end_year']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['job_title', 'company', 'start_year', 'end_year', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }