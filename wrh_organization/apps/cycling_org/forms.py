from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from django.forms import ModelForm, DateInput

from .models import Event, OrganizationMember


class UploadValidateFile(forms.Form):
    validate_file = forms.FileField()


class EventEditForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description']
        # fields = ['name', 'description', 'start_date', 'end_date', 'organizer_email', 'country', 'city', 'state', 
        #           'website', 'registration_website', 'logo', 'tags', 'more_data', 'organization', 'create_by', 'permit_no', 'is_usac_permitted']
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
        fields = ['organization', 'member', 'org_member_uid', 'is_admin',  'is_master_admin', 'membership_price', 
                  'is_active', 'status', 'start_date', 'exp_date', 'member_fields',]
        labels = {'start_date': 'Start Date', 'exp_date': 'Expiration Date'}


class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'at-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'at-input'}))

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
    phone_number = forms.CharField(required=False, validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
                                   label="Phone Number", empty_value=None)
    address1 = forms.CharField(required=False, label="Address 1", empty_value=None)
    address2 = forms.CharField(required=False, label="Address 2", empty_value=None)
    city = forms.CharField(required=False, label="City", empty_value=None)
    state = forms.CharField(required=False, label="State", empty_value=None)
    zip_code = forms.CharField(required=True, label="Zip Code")
    country = forms.CharField(required=False, initial="United States", label="Country", empty_value=None)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")
    #
    #     if password != confirm_password:
    #         self.add_error("confirm_password", "Passwords do not match")
