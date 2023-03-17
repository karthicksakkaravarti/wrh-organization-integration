from typing import Literal

from django.core.exceptions import ObjectDoesNotExist

from .models import Member, OrganizationMember
from ..usacycling.models import USACRiderLicense


def usac_license_on_record(license_number: str) -> str:
    """Verifiy the USAC license number is on record at WRH and that it has been verified."""
    try:
        if license_number == 'ONE DAY':
            return 'ONE DAY'
        l = Member.objects.get(usac_license_number=license_number)
    except ObjectDoesNotExist:
        return 'FALSE'
    except ValueError:
        return 'ERROR'
    if l.usac_license_number_verified:
        return 'TRUE'
    else:
        return 'NOT_VERIFIED'


def valid_usac_licenses(license_number: str) -> str | list[str, ...]:
    """Get status of USAC license number from USAC records (model)"""
    try:
        if license_number == 'ONE DAY':
            return 'ONE DAY'
        licenses = USACRiderLicense.objects.filter(license_number=license_number)
        if not licenses:
            return 'NOT FOUND'
        else:
            return [f"{l.license_type}" for l in licenses if l.license_status.lower() == 'valid']
    except ValueError:
        return 'ERROR'
    except:
        return 'ERROR'


def usac_club_match(license_number: str, club: str) -> str:
    """Get status of persons USAC club from USAC records (model)"""
    try:
        if license_number == 'ONE DAY':
            return 'ONE DAY'
        if club == '':
            return 'NO CLUB'
        licenses = USACRiderLicense.objects.filter(license_number=license_number)
        if not licenses:
            return 'LICENSE NOT FOUND'
        if club in [l.data['club'] for l in licenses]:
            return 'MATCH'
        else:
            return 'NO MATCH'
    except:
        return 'ERROR'


def wrh_club_match(license_number: str, club: str) -> str:
    """Get status of persons WRH club from WRH records (model)"""
    try:
        if license_number == 'ONE DAY':
            return 'ONE DAY'
        if club == '':
            return 'NO CLUB'
        m = Member.objects.get(usac_license_number=license_number)
        clubs = OrganizationMember.objects.filter(member=m)
        if clubs:
            if club in [c.organization.name for c in clubs]:
                return 'MATCH'
            else:
                return 'NO MATCH'
    except ObjectDoesNotExist:
        return 'LICENSE NOT FOUND'
    except:
        return 'ERROR'


def wrh_bc_member(license_number: str) -> str:
    """Get status of persons WRH BC from WRH records (model)"""
    try:
        m = Member.objects.get(usac_license_number=license_number)
        clubs = OrganizationMember.objects.filter(member=m)
        if 'Bicycle Colorado' in [c.organization.name for c in clubs]:
            return 'TRUE'
        else:
            return 'FALSE'
    except ObjectDoesNotExist:
        return 'LICENSE NOT FOUND'
    except:
        return 'ERROR'


def wrh_club_memberships(license_number: str) -> str:
    try:
        m = Member.objects.get(usac_license_number=license_number)
        clubs = OrganizationMember.objects.filter(member=m)
        return [c.organization.name for c in clubs]
    except ObjectDoesNotExist:
        return ''
    except:
        return 'ERROR'


def wrh_email_match(email: str) -> str:
    try:
        m = Member.objects.get(email=email)
        return f"{m.first_name} {m.last_name}"
    except ObjectDoesNotExist:
        return "NOT FOUND"
    except:
        return 'ERROR'


def wrh_local_association(license_number: str) -> list[str] | str:
    try:
        m = USACRiderLicense.objects.filter(license_number=license_number)
        return [t.local_association for t in m]
    except:
        return 'ERROR'


def wrh_usac_clubs(license_number: str) -> list[str] | str:
    try:
        m = USACRiderLicense.objects.filter(license_number=license_number)
        return [t.data['club'] for t in m]
    except:
        return 'ERROR'


def bc_race_ready(license_number: str) -> Literal['TRUE', 'FALSE']:
    usac_member = valid_usac_licenses(license_number) not in ['NOT FOUND', 'ERROR', 'ONE DAY']
    if usac_member:
        return 'TRUE'
    else:
        return 'FALSE'


def bc_individual_cup_ready(license_number: str) -> Literal['TRUE', 'FALSE']:
    # TODO: need to check bc membership type.
    if bc_race_ready == 'TRUE' and wrh_bc_member(license_number) == 'TRUE':
        return 'TRUE'
    else:
        return 'FALSE'


def bc_team_cup_ready(license_number: str, club: str) -> Literal['TRUE', 'FALSE']:
    match_bc = wrh_club_match(license_number, club) == 'MATCH'
    # TODO: Should remove BC from the list.
    match_usac = club in wrh_usac_clubs(license_number)
    ind_ready = bc_individual_cup_ready(license_number) == 'TRUE'
    if match_bc and match_usac and ind_ready:
        return 'TRUE'
    else:
        return 'FALSE'