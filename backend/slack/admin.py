from django.contrib import admin

from slack.models import SlackUser, SlackChannel


class SlackUserAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "member"]
    list_display = ["id", "member"]


@admin.action(description="Refresh Slack channel")
def force_refresh(modeladmin, request, queryset):
    for slack_channel in queryset:
        slack_channel.force_refresh()


class SlackChannelAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "show", "briefing_ts"]
    list_display = ["id", "show"]
    actions = [force_refresh]


admin.site.register(SlackUser, SlackUserAdmin)
admin.site.register(SlackChannel, SlackChannelAdmin)
