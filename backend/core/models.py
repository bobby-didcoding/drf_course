from django.db import models
from utils.model_abstracts import Model
from django_extensions.db.models import (
	TimeStampedModel, # fields like created
	ActivatorModel, # status field, activated date and deactivated date
	TitleDescriptionModel # 2 text fields (char)
)

class Contact(
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
	Model
	):

	class Meta:
		verbose_name_plural = "Contacts"

	email = models.EmailField(verbose_name="Email") #email field

	def __str__(self):
		return f'{self.title}'