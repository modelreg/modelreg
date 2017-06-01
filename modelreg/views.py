#!/usr/bin/env python3

from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.sites.shortcuts import get_current_site

from django.conf import settings

import qrcode

from . import models


def found_info(req):
    """Info for someone who found a model
    """

    return render(req, 'found_info.html')

def found(req, ident, auth):
    """Decoded QR code handler.

    Find correct user / code object via ident, then try to
    decrypt via "auth" tag.
    """

    # TODO: Rate limit requests to this page on a per-client-IP base.
    # We don't want someone to walk across an event for example and
    # scanning all the models.
    # Also, once a request is submitted for a given public profile,
    # we want a rate limit there as well - it's very unlikely that
    # the same owner loses multiple models within a short period of
    # time. The exact values need to be determined in the future.

    code = get_object_or_404(models.PublicProfile, identifier=ident)

    if req.POST:
        if req.POST['finder_email'] != req.POST['finder_email2']:
            # TODO: notify user - email must be confirmed
            pass

        case = models.Case()
        case.model_owner = code.user
        case.reporter_email = req.POST['finder_email']
        case.damage_type    = req.POST['damage_type']

        case.save()

        if req.POST['message']:
            msg = models.CaseMessage()
            msg.case = case
            msg.from_owner = True
            msg.message = req.POST['message']

            msg.save()

        return redirect('case_finder', ident=case.identifier)

    return render(req, 'found.html', {'public_profile': code})

def case_info(case):
    "Return a dict suitable for the case_* views as rendering context"

    messages = case.messages.order_by('timestamp')
    public_profile = case.model_owner.public_profile

    return {
        'case': case,
        'messages': messages,
        'public_profile': public_profile
    }


def case_finder(req, ident):
    case = models.Case.objects.get(identifier=ident)

    if not case.model_owner == req.user:
        # TODO: reject request; owner view does not match
        # current user
        pass

    if req.POST and req.POST['message']:
        msg = models.CaseMessage()
        msg.case = case
        msg.from_owner = False
        msg.message = req.POST['message']
        msg.save()

    return render(req, 'case_finder.html', case_info(case))


def case_owner(req, pk):
    case = models.Case.objects.get(pk=pk)
    if not case.model_owner == req.user:
        # TODO: reject request; owner view does not match
        # current user
        pass

    if req.POST and req.POST['message']:
        msg = models.CaseMessage()
        msg.case = case
        msg.from_owner = True
        msg.message = req.POST['message']
        msg.save()

    return render(req, 'case_owner.html', case_info(case))


def index(req):
    return render(req, 'index.html')


@login_required
def profile(req):

    # If freshly logged in, we may not yet have a profile
    profile, p_created = models.Profile.objects.get_or_create(
        user=req.user
    )
    pprof, pp_created = models.PublicProfile.objects.get_or_create(
        user=req.user
    )

    if req.POST:
        profile.address   = req.POST['address']
        profile.phone     = req.POST['phone']
        pprof.public_info = req.POST['public_info']

        profile.save()
        pprof.save()

    return render(
        req,
        'profile.html',
        {
            'user': req.user,
            'profile': profile,
            'public_profile': pprof,
            'profile_url': profile_url(pprof, req)
        }
    )

def profile_url(pprof, req):
    url = reverse('found', kwargs={'ident': pprof.identifier, 'auth':pprof.auth})

    proto = 'https' if req.is_secure() else 'http'

    domain = get_current_site(req)

    return '%s://%s%s' % (proto, domain, url)

@login_required
def profile_qrcode_img(req):

    pprof, pp_created = models.PublicProfile.objects.get_or_create(
        user=req.user
    )
    response = HttpResponse(content_type="image/png")

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M
    )

    qr.add_data(profile_url(pprof, req))

    qr.make(fit=True)

    img = qr.make_image()

    img.save(response, 'png')
    return response


@login_required
def system_update(req):
    import uwsgi
    import git
    from django.core.management import call_command

    git_cmd = git.cmd.Git(settings.BASE_DIR)
    git_cmd.pull()

    call_command('migrate')

    uwsgi.reload()
    return render(req, 'system_update.html')
