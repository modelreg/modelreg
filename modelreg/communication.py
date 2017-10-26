#!/usr/bin/env python3

"""Documentation about the module... may be multi-line"""

from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

def _uri(request, view, *args, **kwargs):
    return request.build_absolute_uri(reverse(view, args=args, kwargs=kwargs))


def new_case(request, msg):
    """Notify both owner and finder about a found model

    Pass in a request and a CaseMessage as parameters.
    """
    notify_owner (request, msg, 'found')
    notify_finder(request, msg, 'found')

def notify_owner(request, msg, tag='update'):
    """Notify the owner of an update regarding the current case.

    Pass in a request and a CaseMessage as parameters.
    """
    return _notify(
        request,
        msg,
        msg.case.model_owner.email,
        'notify_owner_%s' % tag)


def notify_finder(request, msg, tag='update'):
    """Notify the finder of an update regarding the current case.

    Pass in a request and a CaseMessage as parameters.
    """
    return _notify(
        request,
        msg,
        msg.case.reporter_email,
        'notify_finder_%s' % tag)


def notify_admin(request, msg, triggered_by):
    """Notify the admin that a case has been escalated.

    Pass in a request and a CaseMessage as parameters.
    """
    admins = User.objects.filter(is_superuser=True)

    for admin in admins:
        _notify(
            request,
            msg,
            admin.email,
            template_prefix='notify_admin',
            triggered_by=_(triggered_by)
        )


def _notify(request, msg, recipient, template_prefix='notify_owner', **kwargs):

    context = {}
    context.update(kwargs)
    context.update({
        'case':     msg.case,
        'message':  msg.message,
        'owner':    msg.case.model_owner,
        'operator': settings.SYSTEM_OPERATOR,

        'owner_link':  _uri(request, 'case_owner',  msg.case.pk),
        'admin_link':  _uri(request, 'case_admin',  msg.case.pk),
        'finder_link': _uri(request, 'case_finder', msg.case.identifier),
    })


    subject = render_to_string('modelreg/%s_subject.txt' % template_prefix,
                               context)
    # Force subject to a single line to avoid header-injection
    # issues.
    subject = ''.join(subject.splitlines())

    message = render_to_string('modelreg/%s.txt' % template_prefix,
                               context)

    send_mail(
        subject,
        message,
        settings.SYSTEM_EMAIL,
        [recipient]
    )
