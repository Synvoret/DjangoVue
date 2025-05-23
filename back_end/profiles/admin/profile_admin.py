from django.contrib import admin

from profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ["user", "user_email", "website", "bio"]

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"
