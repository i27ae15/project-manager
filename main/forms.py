from django import forms

class Comment(forms.Form):
    comment = forms.CharField(label='Make a new comment', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # project_id = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'type': 'hidden'}))
    

class AnswerComment(forms.Form):
    comment = forms.CharField(label='', widget=forms.TextInput(attrs={'style': 'display:none'}))
    answer = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))


class NewActivity(forms.Form):
    activity = forms.CharField(label='', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control timeline-inputs'}))


class PersonalDetails(forms.Form):
    first_name = forms.CharField(label='First name', max_length=30)
    last_name = forms.CharField(label='Last name', max_length=30)
    email = forms.EmailField(label='Email', max_length=50)
    phone = forms.CharField(label='Phone', max_length=30)
    website = forms.CharField(label='Website URL', max_length=150)
    about_me = forms.CharField(label='About Me', max_length=300)
    city = forms.CharField(label='City', max_length=30)
    country = forms.CharField(label='Country', max_length=30)
