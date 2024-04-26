from django.db.models import *
from hashlib import md5


class User(Model):
    icon = ImageField()
    user_id = PositiveBigIntegerField()
    balance = PositiveBigIntegerField()
    ref_link = CharField(max_length=256)
    wallet_address = CharField(max_length=256)
    energy = PositiveBigIntegerField()
    energy_limit = PositiveBigIntegerField()
    level = PositiveSmallIntegerField()
    bonus = PositiveBigIntegerField()
    tap_step = PositiveSmallIntegerField()
    refered_by = ManyToManyField("self", related_name="friends", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user_id}"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'

class Harem(Model):
    key = CharField(max_length=256)
    name = CharField(max_length=128, unique=True)
    owner = ForeignKey(User, on_delete=CASCADE, related_name='harem')
    balance = PositiveBigIntegerField(default=0, blank=True)
    target = PositiveBigIntegerField()
    members = ManyToManyField(User, related_name="harems")

    def validate_key(self, key: str):
        return self.key == md5(key)
    
    def set_key(self, key: str):
        self.key = md5(key)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'harem'
        verbose_name_plural = 'harems'
        db_table = 'harems'
