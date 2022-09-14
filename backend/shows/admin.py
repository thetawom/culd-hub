from django.contrib import admin

from shows.models import Show, Round, Member, Contact, Role


class RoundInlineAdmin(admin.TabularInline):
    model = Round


class RoleInlineAdmin(admin.TabularInline):
    model = Role


class ShowAdmin(admin.ModelAdmin):
    @staticmethod
    def rounds(show):
        count = show.rounds.count()
        return count if count > 0 else None

    list_display = [
        "name",
        "status",
        "has_slack_channel",
        "priority",
        "day_of_week",
        "date",
        "formatted_time",
        "lions",
        "performer_count",
        "rounds",
        "address",
    ]
    empty_value_display = "TBD"

    inlines = [RoundInlineAdmin, RoleInlineAdmin]


class MemberAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "position",
        "school",
        "class_year",
    ]


class MemberInlineAdmin(admin.TabularInline):
    model = Member


admin.site.register(Show, ShowAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Contact)
admin.site.register(Role)
