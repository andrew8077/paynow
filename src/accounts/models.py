from django.db import models
import uuid
from organizations.abstract import (
    AbstractOrganization,
    AbstractOrganizationUser,
    AbstractOrganizationOwner,
    AbstractOrganizationInvitation
)
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Account(AbstractOrganization):
    name = models.CharField(max_length=75, unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    collected_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, editable=False)
    expected_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, editable=False)


class OrgUser(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    organization_id = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    organization_name = models.CharField(max_length=75, default="NO ORG")
    is_owner = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    amount_owed = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Organization Member"


class AccountUser(AbstractOrganizationUser):
    pass


class AccountOwner(AbstractOrganizationOwner):
    pass


class AccountInvitation(AbstractOrganizationInvitation):
    pass