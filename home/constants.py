from django.utils.translation import gettext_lazy as _

TYPE_LOG = (
    ('sms', _('SMS')),
    ('capture', _('Capture screen')),
    ('location', _('Get Location')),
    ('optimize', _('Optimize Battery'))
)
TYPE_ACTIVITY = (
    ('capture_loop', _('Loop capture')),
    ('capture', _('Capture screen')),
    ('location', _('Get Location')),
    ('optimize', _('Optimize Battery'))
)
GENDER = (
    ('male', _('Male')), 
    ('female', _('Female')), 
    ('unknow', _('Unknow'))
)