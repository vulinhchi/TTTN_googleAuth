from django.db import models
from django.contrib.auth.models import User #phai co dong nay, mac du k co model nao moi

from datetime import datetime

class Question(models.Model):
	name_asker = models.CharField(('Can I have your name, genius?'), max_length = 50)
	content = models.TextField()
	id_user_receive = models.ForeignKey(User, on_delete = models.CASCADE, related_name='question_ahihi')
	answer = models.TextField(blank = True, null= True)
	asking_day = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.content
