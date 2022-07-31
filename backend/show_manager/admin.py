from django.contrib import admin

from .models import Show, Round, Member, Contact, Role


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
        "priority",
        "day_of_week",
        "date",
        "format_time",
        "lions",
        "num_performers",
        "rounds",
        "address",
        "is_published",
        "is_open",
    ]
    empty_value_display = "TBD"

    inlines = [RoundInlineAdmin, RoleInlineAdmin]


class MemberAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "membership",
        "school",
        "class_year",
    ]


class MemberInlineAdmin(admin.TabularInline):
    model = Member


admin.site.register(Show, ShowAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Contact)
admin.site.register(Role)
