from django.contrib import admin

from slack.models import SlackUser, SlackChannel


class SlackUserAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "member"]
    list_display = ["id", "member"]


@admin.action(description="Refresh Slack channels")
def force_refresh(modeladmin, request, queryset):
    for slack_channel in queryset:
        slack_channel.force_refresh()


@admin.action(description="Archive Slack channels")
def archive(modeladmin, request, queryset):
    for slack_channel in queryset:
        slack_channel.archive(rename=False)


class SlackChannelAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "show", "briefing_ts", "is_archived"]
    list_display = ["id", "show", "is_archived"]
    actions = [force_refresh, archive]


admin.site.register(SlackUser, SlackUserAdmin)
admin.site.register(SlackChannel, SlackChannelAdmin)
