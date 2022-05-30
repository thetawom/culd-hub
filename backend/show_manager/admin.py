from django.contrib import admin
from .models import Show, Round, Member, Contact, Role


class RoundInlineAdmin(admin.TabularInline):
    model = Round


class RoleInlineAdmin(admin.TabularInline):
    model = Role


class ShowAdmin(admin.ModelAdmin):
    def rounds(self, obj):
        count = obj.round_set.count()
        return count if count > 0 else None

    list_display = [
        "name",
        "day_of_week",
        "date",
        "format_time",
        "lions",
        "rounds",
        "address",
    ]
    empty_value_display = "TBD"
    ordering = ["date", "time"]

    inlines = [RoundInlineAdmin, RoleInlineAdmin]


admin.site.register(Show, ShowAdmin)
admin.site.register(Member)
admin.site.register(Contact)
admin.site.register(Role)
