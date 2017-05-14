#!/usr/bin/env python3

from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.contrib.sites.shortcuts import get_current_site

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

    code = get_object_or_404(models.PublicProfile, pk=int(ident, 36))

    data = code.get_data(auth)

    return render(req, 'found.html', {'public_profile': data})


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
            'public_profile': pprof
        }
    )

@login_required
def profile_qrcode_img(req):

    pprof, pp_created = models.PublicProfile.objects.get_or_create(
        user=req.user
    )
    response = HttpResponse(content_type="image/png")

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L
    )

    url = reverse('found', kwargs={'ident': pprof.identifier, 'auth':pprof.auth})

    proto = 'https' if req.is_secure() else 'http'

    domain = get_current_site(req)

    qr.add_data('%s://%s%s' % (proto, domain, url))

    qr.make(fit=True)

    img = qr.make_image()

    img.save(response, 'png')
    return response
