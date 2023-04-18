from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm, DateInput
from turnstile.fields import TurnstileField

from .models import Event, OrganizationMember, Organization
from ..wrh_account.models import User


class UploadValidateFile(forms.Form):
    validate_file = forms.FileField()


class EventEditForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date', 'end_date', 'organizer_email', 'country', 'city', 'state',
                  'website', 'registration_website', 'logo', 'tags', 'more_data', 'organization', 'permit_no',
                  'is_usac_permitted', 'organization', 'publish_type']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'name': 'Event Name',
            'start date': 'Start Date',
            'end_date': 'End Date',
            'description': 'Description',
            'organizer_email': 'Event Email',
            'website': 'Event Website',
            'registration_website': 'Registration Website',
            'is_usac_permitted': 'Is USAC Permitted',
            'permit_no': 'Permit Number',
            'city': 'City',
            'state': 'State',
            'country': 'Country',
        }
        help_texts = {
            'name': 'Enter the name of the event.',
            'start_date': 'Enter the Start date of the event.',
            'end_date': 'Enter the end date of the event.',
            'description': 'Enter a short description of the event.',
            'organizer_email': 'Enter the email of the event organizer.',
            'website': 'Enter the website of the event.',
            'registration_website': 'Enter the registration website of the event.',
            'is_usac_permitted': 'Is the event USAC permitted?',
            'permit_no': 'Enter the permit number of the event.',
            'city': 'Enter the nearest city of the start.',
            'state': 'Enter the state of the start.',
            'country': 'Enter the country of the start.',
        }

        error_messages = {
            'name': {
                'max_length': 'This event name is too long.',
            },
        }


class JoinClubForm(ModelForm):
    class Meta:
        model = OrganizationMember
        fields = ['organization', 'member', 'org_member_uid', 'is_admin', 'is_master_admin', 'membership_price',
                  'is_active', 'status', 'start_date', 'exp_date', 'member_fields', ]
        labels = {'start_date': 'Start Date', 'exp_date': 'Expiration Date'}


class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'at-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'at-input'}))
    turnstile = TurnstileField()


class SignUpForm(forms.Form):
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")
    date_of_birth = forms.DateField(required=True, label="Date of Birth", widget=DateInput(attrs={'type': 'date'}))
    usac_number = forms.CharField(required=False, label="USAC Number", empty_value=None)
    gender = forms.ChoiceField(choices=[('', 'Select Gender'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
                               required=False)
    waiver_accepted = forms.BooleanField(label="I accept the waiver", required=True, widget=forms.CheckboxInput())
    terms_of_service = forms.BooleanField(label="I agree to Terms and Service", required=True,
                                          widget=forms.CheckboxInput())
    opt_out_email = forms.BooleanField(label="Opt out of promotional emails", widget=forms.CheckboxInput())
    turnstile = TurnstileField(label="")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is no user registered with the specified email address.")
        return email


class EditClub(ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'website', 'type', 'social_media', 'phone', 'email', 'address', 'country', 'city', 'state',
                  'zipcode', 'about', 'logo', 'waiver_text', 'approved']

        labels = {
            'name': 'Club Name',
            'type': 'Club, Promoter',
        }
        help_texts = {
            'name': 'Enter the name of the club.',
            'type': 'Choose a Organization type',
        }
        error_messages = {}
