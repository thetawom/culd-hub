from django.contrib import admin

from slack.models import SlackUser, SlackChannel


class SlackUserAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "member"]
    list_display = ["id", "member"]


class SlackChannelAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "show", "briefing_ts"]
    list_display = ["id", "show"]


admin.site.register(SlackUser, SlackUserAdmin)
admin.site.register(SlackChannel, SlackChannelAdmin)
