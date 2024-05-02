from django.db.models import *
from user.models import User

class Button(Model):
    icon = ImageField(upload_to='button/')
    name = CharField(max_length=64, unique=True)
    short_description = CharField(max_length=1024, null=True)
    description = TextField(null=True)
    price = PositiveBigIntegerField()
    level = PositiveSmallIntegerField()
    tap_step = PositiveSmallIntegerField()
    bonus = PositiveBigIntegerField()
    users = ManyToManyField(User, related_name="buttons", blank=True)
    seconds = PositiveSmallIntegerField(default=10)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'button'
        verbose_name_plural = 'buttons'
        db_table = 'buttons'


class Channel(Model):
    icon = ImageField(upload_to='channels/avatar/')
    name = TextField()
    link = TextField()
    bonus = PositiveIntegerField()
    expires_at = DateField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'channel'
        verbose_name_plural = 'channels'
        db_table = 'channels'
