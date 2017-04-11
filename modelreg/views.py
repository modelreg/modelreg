#!/usr/bin/env python3

from django.shortcuts import get_object_or_404, render

from . import models


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
