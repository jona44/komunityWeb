from django.contrib import admin
from .models import Profile, CustomUser, DeviceToken, Notification


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user_email', 'phone', 'is_verified', 'is_active', 'is_complete', 'created_at')
    search_fields = ('first_name', 'surname', 'phone', 'user__email')
    list_filter = ('is_verified', 'is_active', 'is_complete', 'is_deceased')
    readonly_fields = ('created_at', 'updated_at')

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'is_email_verified', 'date_joined')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_active', 'is_email_verified', 'date_joined')
    readonly_fields = ('date_joined', 'last_login')


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'is_active', 'created_at')
    search_fields = ('user__email', 'token')
    list_filter = ('platform', 'is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'title', 'notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__email', 'title', 'message')
    list_filter = ('is_read', 'notification_type', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


