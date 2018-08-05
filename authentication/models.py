from django.db import models
from django.contrib.auth.models import User #phai co dong nay, mac du k co model nao moi
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

class Question(models.Model):
	name_asker = models.CharField(('Can I have your name, genius?'), max_length = 50)
	content = models.TextField()
	id_user_receive = models.ForeignKey(User, on_delete = models.CASCADE, related_name='question_ahihi')
	answer = models.TextField(blank = True, null= True)
	asking_day = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.content

class Captcha(models.Model):
	picture = models.ImageField(upload_to='picture/', blank=True, null=True)
	code_captcha = models.CharField(_('code_captcha'), max_length=250)
