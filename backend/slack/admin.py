from django.contrib import admin

from slack.models import User, Channel

admin.site.register(User)
admin.site.register(Channel)
