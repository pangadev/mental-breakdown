from django import forms
from crm.models import RelationshipType, Contact
from model_utils import Choices
from django.contrib.auth.models import User

relationship_types = RelationshipType.objects.all()


class ContactForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    # birthday = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'birthdate', 'sex', 'description', 'avatar',]

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'birthdate': forms.DateInput(attrs={'class': 'datepicker'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Description'}),

        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        # self.created_by = kwargs.pop('created_by', None)
        # self.fields['sex'].empty_label = "(Select here)"


# class ContactForm(forms.Form):
#     first_name = forms.CharField(label="First name", widget=forms.TextInput(attrs={'placeholder': 'First name'}))
#     last_name = forms.CharField(label="Last name", widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
#     birthdate = forms.DateTimeField(label="Birthday", widget=forms.TextInput(attrs={'placeholder': 'Birthday'}))
#     sex = forms.CharField(label="Sex",
#                           widget=forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Unsure', 'Unsure')]))
#     description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'placeholder': 'Description'}))
#     avatar = forms.ImageField(label="Avatar")

class ActivityForm(forms.Form):
    title = forms.CharField(label="Activity title", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(label="Activity title", widget=forms.Textarea(attrs={'placeholder': 'Description'}))


class RelationshipTypeForm(forms.Form):
    name = forms.CharField(label="Relationship name",
                           widget=forms.TextInput(attrs={'placeholder': 'Relationship name'}))
    from_type = forms.CharField(label="Contact A title",
                                widget=forms.TextInput(attrs={'placeholder': 'Contact A title'}))
    to_type = forms.CharField(label="Contact B title", widget=forms.TextInput(attrs={'placeholder': 'Contact B title'}))


class ContactRelationshipForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     my_arg = kwargs.pop('my_arg')
    #     super(ContactRelationshipForm, self).__init__(*args, **kwargs)
    #     self.fields['to_contact'] = forms.ModelChoiceField(queryset=Contact.objects.exclude(id=my_arg),
    #                                                        empty_label=None)
    #
    # # types = forms.ModelChoiceField(queryset=q3)
    # types = forms.ModelChoiceField(queryset=RelationshipType.objects.all(), to_field_name="from_type", empty_label=None)
    # # types = forms.ChoiceField(widget=forms.RadioSelect, choices=["Dziecko", "Pracownik"])
    #
    def __init__(self, *args, **kwargs):
        my_arg = kwargs.pop('my_arg')
        user = kwargs.pop('user')
        super(ContactRelationshipForm, self).__init__(*args, **kwargs)
        self.fields['contact'] = forms.ModelChoiceField(queryset=Contact.objects.exclude(id=my_arg).filter(created_by=user), empty_label=None)

    TYPE_CHOICES = Choices("Rodzic", "Dziecko", "Pracownik", "Pracodawca", "Przyjaciel", "Przyjaciel")

    types = forms.ChoiceField(choices=TYPE_CHOICES)


class NavbarForm(forms.Form):
    name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Search'}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class CreateUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))
    name = forms.CharField(label='Name', max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label='Last name', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(label='email', max_length=100,
                             widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Hasła nie pasują"
            )
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Nazwa użytkownika jest zajęta"
            )
        return username


class ForgottenPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Hasła nie pasują"
            )
        return password2
