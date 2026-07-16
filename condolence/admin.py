from django.contrib import admin
from .models import Contribution, Deceased, FundCampaign, CampaignContribution


@admin.register(Deceased)
class DeceasedAdmin(admin.ModelAdmin):
    list_display = ('deceased', 'group', 'date', 'cont_is_active', 'contributions_open', 'funds_disbursed')
    search_fields = ('deceased__first_name', 'deceased__surname', 'group__name')
    list_filter = ('cont_is_active', 'contributions_open', 'funds_disbursed', 'date')
    date_hierarchy = 'date'
    readonly_fields = ('date',)
    raw_id_fields = ('deceased', 'group', 'group_admin', 'beneficiary')
    fieldsets = (
        ('Member Info', {
            'fields': ('deceased', 'group', 'group_admin')
        }),
        ('Campaign Status', {
            'fields': ('cont_is_active', 'contributions_open', 'funds_disbursed')
        }),
        ('Payout', {
            'fields': ('beneficiary',)
        }),
        ('Timestamps', {
            'fields': ('date',),
            'classes': ('collapse',),
        }),
    )


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('contributing_member', 'deceased_member', 'group', 'amount', 'payment_method', 'contribution_date')
    search_fields = (
        'contributing_member__first_name', 'contributing_member__surname',
        'group__name', 'deceased_member__deceased__first_name'
    )
    list_filter = ('payment_method', 'contribution_date', 'group')
    date_hierarchy = 'contribution_date'
    readonly_fields = ('contribution_date',)
    raw_id_fields = ('group', 'deceased_member', 'contributing_member', 'group_admin', 'transaction')


@admin.register(FundCampaign)
class FundCampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'campaign_type', 'group_or_org', 'target_amount', 'is_public', 'contributions_open', 'funds_disbursed', 'created_at', 'deadline')
    search_fields = ('title', 'description', 'group__name', 'organisation__name')
    list_filter = ('campaign_type', 'contributions_open', 'funds_disbursed', 'is_public', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    raw_id_fields = ('group', 'organisation', 'beneficiary', 'created_by')
    fieldsets = (
        ('Campaign Details', {
            'fields': ('title', 'description', 'campaign_type')
        }),
        ('Association', {
            'fields': ('group', 'organisation', 'beneficiary', 'created_by')
        }),
        ('Funding', {
            'fields': ('target_amount', 'is_public', 'contributions_open', 'funds_disbursed', 'deadline')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def group_or_org(self, obj):
        if obj.group:
            return f'Group: {obj.group.name}'
        if obj.organisation:
            return f'Org: {obj.organisation.name}'
        return '-'
    group_or_org.short_description = 'Group / Organisation'


@admin.register(CampaignContribution)
class CampaignContributionAdmin(admin.ModelAdmin):
    list_display = ('contributing_member', 'campaign', 'amount', 'payment_method', 'contribution_date')
    search_fields = ('contributing_member__first_name', 'contributing_member__surname', 'campaign__title')
    list_filter = ('payment_method', 'contribution_date')
    date_hierarchy = 'contribution_date'
    readonly_fields = ('contribution_date',)
    raw_id_fields = ('campaign', 'group', 'organisation', 'contributing_member', 'transaction')

