from django.core.management.base import BaseCommand
from chema.models import Group, GroupMembership


class Command(BaseCommand):
    help = (
        'Scan all active groups and ensure every creator has an active admin '
        'GroupMembership. Safe to run repeatedly.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fixed without making changes.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - no changes will be saved.\n'))

        fixed = 0
        skipped = 0

        for group in Group.objects.filter(is_active=True).select_related('creator'):
            if not group.creator:
                skipped += 1
                continue

            try:
                creator_profile = group.creator.profile
            except Exception:
                self.stdout.write(
                    self.style.WARNING(
                        f'  SKIP: No profile for creator of "{group.name}" (ID:{group.id})'
                    )
                )
                skipped += 1
                continue

            membership = GroupMembership.objects.filter(
                group=group, member=creator_profile
            ).first()

            if membership is None:
                self.stdout.write(
                    f'  [NO MEMBERSHIP]  "{group.name}" (ID:{group.id}) -- '
                    f'Creator: {group.creator.email}'
                )
                if not dry_run:
                    GroupMembership.objects.create(
                        group=group,
                        member=creator_profile,
                        is_admin=True,
                        role='admin',
                        status='active',
                        is_active=True,
                    )
                fixed += 1
                continue

            needs_fix = (
                not membership.is_admin
                or membership.role not in ('admin', 'moderator')
                or membership.status != 'active'
                or not membership.is_active
            )

            if needs_fix:
                self.stdout.write(
                    f'  [BAD MEMBERSHIP] "{group.name}" (ID:{group.id}) -- '
                    f'{creator_profile.full_name} | '
                    f'is_admin={membership.is_admin} role={membership.role} '
                    f'status={membership.status} is_active={membership.is_active}'
                )
                if not dry_run:
                    membership.is_admin = True
                    membership.role = 'admin'
                    membership.status = 'active'
                    membership.is_active = True
                    membership.save()
                fixed += 1

        verb = 'Would fix' if dry_run else 'Fixed'
        if fixed == 0:
            self.stdout.write(self.style.SUCCESS(
                f'\nAll groups OK. Skipped {skipped}.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'\n{verb} {fixed} group(s). Skipped {skipped}.'
            ))
