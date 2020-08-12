import datetime

from django.forms import ModelForm
from catalog.models import BookInstance
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookModelForm(ModelForm):
  """docstring for RenewBookModelForm"""
  def clean_due_back(self):
    data = self.cleaned_data['due_back']

    if data < datetime.date.today():
      raise ValidationError(_('Invalid date - renewal in past'))

    if data > datetime.date.today() + datetime.timedelta(weeks =4):
      raise ValidationError(_('Invalid date - renewal more than 4 weeks'))

    return data

  class Meta:
    model = BookInstance
    fields = ['due_back']
    labels={'due_back': _('New renewal date')}
    help_text={'due_back': _('Enter a date between now and 4 weeks(default 3).')}