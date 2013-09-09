from django.db import models
from upy.contrib.cked.fields import RichTextField
from django.utils.translation import ugettext_lazy as _

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError: # django < 1.5
    from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(_(u'Nome'), max_length=255)
    disabled = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Stanza')
        verbose_name_plural = _(u'Stanze')

class Message(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'Utente'))
    room = models.ForeignKey(Room, verbose_name=_(u'Stanza'))
    message = RichTextField(_(u'Messaggio'))
    creation_date = models.DateTimeField(_(u'Data creazione'), auto_now_add=True)
    disabled = models.BooleanField(default=False)

    def __unicode__(self):
        return "messaggio"

    class Meta:
        verbose_name = _(u'Messaggio')
        verbose_name_plural = _(u'Messaggi')
