from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField  # PostgreSQL을 사용하는 경우
import uuid


class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True)
    # 다음은 전체 대화에 대한 JSON 필드입니다.
    conversation = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " - " + str(self.conversation)
