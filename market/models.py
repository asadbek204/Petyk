from django.db.models import *


class Button(Model):
    icon = ImageField(upload_to='button/icons/')
    name = CharField(max_length=64)
    level = PositiveSmallIntegerField()
    tap_step = PositiveSmallIntegerField()

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
