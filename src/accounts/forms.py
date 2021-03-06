from django import forms
from .models import Account, AccountUser, OrgUser, InvoiceHistory, Budget, Category
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.models import Site
from organizations.backends import invitation_backend
from organizations.backends.forms import UserRegistrationForm
from django.conf import settings


class NewOrgForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Organization Name'),
        widget=forms.TextInput(attrs={'placeholder': "Name of Organization"}),
        error_messages={'required': 'Required.'}
    )

    class Meta:
        model = Account
        fields = ('name', )
        exclude = {'slug', 'id', 'collected_amount', 'expected_amount'}

    def save(self, commit=True):
        user = super(NewOrgForm, self).save(commit=False)
        user.name = self.cleaned_data['name']
        if commit:
            user.save()
        return user


class NewUserAdminForm(UserCreationForm):
    """
    The user that is created alongside the organization.
    Becomes the owner of the organization which grants this user
    more permissions.
    """
    username = forms.CharField(
        strip=True,
        error_messages={'required': "Required."},
        widget=forms.TextInput(attrs={'placeholder': 'Enter a Username For the Admin Account'})
    )
    email = forms.EmailField(
        max_length=75,
        error_messages={'required': "Required."},
        widget=forms.TextInput(attrs={'placeholder': 'Enter a Valid Email Address'})
    )


    class Meta:
        model = OrgUser
        fields = ("username", "email", "password1", "password2")
        exclude = ['organization_id',
                   'organization_name',
                   'is_owner', 'is_member',
                   'amount_owed', 'amount_paid',
                   'has_stripe_account', 'stripe_account_id']


    def save(self, commit=True):
        user = super(NewUserAdminForm, self).save(commit=False)
        self.username = self.cleaned_data['username']
        self.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewUserForm(UserCreationForm):
    """
    Similar to NewUserAdminForm, however, is the basic member with
    no privileges.
    """
    username = forms.CharField(
        strip=True,
        error_messages={'required': "Required."},
        widget=forms.TextInput(attrs={'placeholder': 'Enter a Username'})
    )
    email = forms.EmailField(
        max_length=75,
        error_messages={'required': "Required."},
        widget=forms.TextInput(attrs={'placeholder': 'Enter a Valid Email Address'})
    )

    first_name = forms.CharField(
        max_length=30,
        error_messages={'required': 'Required.'},
        widget=forms.TextInput(attrs={'placeholder': 'Enter Your First Name'})
    )

    last_name = forms.CharField(
        max_length=50,
        error_messages={'required': 'Required.'},
        widget=forms.TextInput(attrs={'placeholder': 'Enter Your Last Name'})
    )

    class Meta:
        model = OrgUser
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        exclude = [
            'organization_id', 'organization_name',
            'is_owner', 'is_member', 'amount_owed', 'amount_paid',
            'has_stripe_account'
        ]

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        self.first_name = self.cleaned_data['first_name']
        self.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UpdateUsernameForm(forms.Form):
    new_username = forms.CharField(
        strip=True,
        error_messages={'required': "Required."},
        widget=forms.TextInput(attrs={'placeholder': 'Enter a Username'})
    )

    class Meta:
        model = OrgUser
        fields = ("new_username",)
        exclude = [
            'organization_id', 'organization_name',
            'is_owner', 'is_member', 'amount_owed', 'amount_paid',
            'has_stripe_account', 'stripe_account_id'
        ]


class RemoveMemberForm(forms.Form):

    member_list = forms.MultipleChoiceField(
        label=_("Member List"),
        help_text="Press and Hold command (mac) / Control (windows) to Select Multiple Members"
    )

    def __init__(self, member_choices=None, *args, **kwargs):
        super(RemoveMemberForm, self).__init__(*args, **kwargs)
        if member_choices is not None:
            self.fields['member_list'].choices = member_choices


class DeleteBudgetForm(forms.Form):
    budget_list = forms.MultipleChoiceField(
        label=_("Budget List"),
        help_text="Press and Hold command (mac) / Control (windows) to Select Multiple Budgets"
    )

    def __init__(self, budget_choices=None, *args, **kwargs):
        super(DeleteBudgetForm, self).__init__(*args, **kwargs)
        if budget_choices is not None:
            self.fields['budget_list'].choices = budget_choices


class SendInvoiceForm(forms.Form):

    member_list = forms.MultipleChoiceField(
        label=_("Member List"),
        help_text="Press and Hold Command (mac) / Control (windows) to Select Multiple Members"
    )

    amount = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        label=_('Amount $'),
        widget=forms.TextInput(attrs={'placeholder': '$0.00'})
    )

    description = forms.CharField(
        widget=forms.Textarea,
        max_length=500,
        label=_("Description of Invoice"),
    )

    def __init__(self, member_choices=None, *args, **kwargs):
        super(SendInvoiceForm, self).__init__(*args, **kwargs)
        if member_choices is not None:
            self.fields['member_list'].choices = member_choices

    class Meta:
        model = InvoiceHistory
        fields = ("member_list", "invoice_amount", "description", "organization_name")
        exclude = ['date_sent']


class CreateBudgetForm(forms.Form):
    title = forms.CharField(max_length=25)

    class Meta:
        model = Budget
        fields = ('title',)
        exclude = {'organization_name', 'total'}


class AddCategoryForm(forms.Form):
    title = forms.CharField(max_length=25)
    amount = forms.DecimalField(max_digits=8, decimal_places=2)
    budget = forms.CharField(max_length=25, label="Budget Title")

    class Meta:
        model = Category
        fields = ('title', 'amount', 'budget')


class EditBudgetForm(forms.Form):

    budget_list = forms.MultipleChoiceField(label=_("Budget List"))
    category = forms.CharField(max_length=25)
    amount = forms.DecimalField(max_digits=8, decimal_places=2)

    def __init__(self, budget_choices=None, *args, **kwargs):
        super(EditBudgetForm, self).__init__(*args, **kwargs)
        if budget_choices is not None:
            self.fields['budget_list'].choices = budget_choices

    class Meta:
        model = Budget
        fields = ("budget_list", "category", "amount")
        exclude = ['total']



class UserInviteForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )


class AccountUserForm(forms.ModelForm):
    """
    Form class for editing OrganizationUsers *and* the linked user model.
    """
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        exclude = ('user', 'is_admin')
        model = AccountUser

    def __init__(self, *args, **kwargs):
        super(AccountUserForm, self).__init__(*args, **kwargs)
        if self.instance.pk is not None:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        """
        This method saves changes to the linked user model.
        """
        if self.instance.pk is None:
            site = Site.objects.get(pk=settings.SITE_ID)
            self.instance.user = invitation_backend().invite_by_email(
                self.cleaned_data['email'],
                **{'first_name': self.cleaned_data['first_name'],
                   'last_name': self.cleaned_data['last_name'],
                   'organization': self.cleaned_data['organization'],
                   'domain': site})
            self.instance.user.first_name = self.cleaned_data['first_name']
            self.instance.user.last_name = self.cleaned_data['last_name']
            self.instance.user.email = self.cleaned_data['email']
            self.instance.user.save()

            return super(AccountUserForm, self).save(*args, **kwargs)


class RegistrationForm(UserRegistrationForm):
    """
    Form class that allows a user to register after clicking through an
    invitation.
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password != password_confirm or not password:
            raise forms.ValidationError("Your password entries must match")
        return super(RegistrationForm, self).clean()
