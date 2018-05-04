from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from account.models import Respondent, RegionalAdmin


User = get_user_model()

user_fields = forms.models.fields_for_model(model=User)

UsernameField = user_fields['username']
FirstNameField = user_fields['first_name']
LastNameField = user_fields['last_name']
IsActiveField = user_fields['is_active']


class RespondentCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    username = UsernameField
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    first_name = FirstNameField
    last_name = LastNameField
    is_active = IsActiveField

    class Meta:
        model = Respondent
        exclude = ['user']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            is_active=True,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        user.set_password(self.cleaned_data['password1'])
        user.save()
        respondent = super().save(commit=False)
        respondent.user = user
        if commit:
            respondent.save()
        return respondent


class RespondentChangeForm(forms.ModelForm):
    username = UsernameField
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"{}\">this form</a>."
        ),
    )
    first_name = FirstNameField
    last_name = LastNameField
    is_active = IsActiveField

    class Meta:
        model = Respondent
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance.user
        self.fields['username'].initial = user.username
        self.fields['password'].initial = user.password
        self.fields['password'].help_text = self.fields['password'].help_text.format("../password/")  # noqa
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['is_active'].initial = user.is_active

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        if "password" in self.initial.keys():
            return self.initial["password"]

    def save(self, commit=True):
        respondent = super().save(commit=False)
        user = respondent.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = self.cleaned_data['is_active']
        user.save()
        if commit:
            respondent.save()
        return respondent


class RegionalAdminCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    username = UsernameField
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    first_name = FirstNameField
    last_name = LastNameField
    is_active = IsActiveField

    class Meta:
        model = RegionalAdmin
        exclude = ['user']
        fields = ['username', 'password1', 'password2', 'first_name',
                  'last_name', 'region', 'is_active']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            is_active=True,
            is_staff=True,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        user.set_password(self.cleaned_data['password1'])
        user.save()
        regionaladmin = super().save(commit=False)
        regionaladmin.user = user
        if commit:
            regionaladmin.save()
        return regionaladmin


class RegionalAdminChangeForm(forms.ModelForm):
    username = UsernameField
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"{}\">this form</a>."
        ),
    )
    first_name = FirstNameField
    last_name = LastNameField
    is_active = IsActiveField

    class Meta:
        model = RegionalAdmin
        exclude = ['user']
        fields = ['username', 'password', 'first_name', 'last_name', 'region',
                  'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance.user
        self.fields['username'].initial = user.username
        self.fields['password'].initial = user.password
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['is_active'].initial = user.is_active

    def save(self, commit=True):
        regionaladmin = super().save(commit=False)
        user = regionaladmin.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = self.cleaned_data['is_active']
        user.save()
        if commit:
            regionaladmin.save()
        return regionaladmin
