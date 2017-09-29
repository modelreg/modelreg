#!/usr/bin/env python3

"""Documentation about the module... may be multi-line"""

from registration.backends.hmac.views import RegistrationView as BaseRegistrationView
from django.contrib.sites.shortcuts import get_current_site

class RegistrationView(BaseRegistrationView):
    def get_email_context(self, activation_key):
        context = super().get_email_context(activation_key)

        import ipdb
        ipdb.set_trace()

        schema = 'https' if self.request.is_secure() else 'http'

        domain = get_current_site(self.request).domain

        context['base_url'] = '%s://%s' % (schema, domain)

        return context
