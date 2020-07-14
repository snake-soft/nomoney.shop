from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from config.settings import VERSION
from chat.models import Chat
from .models import VirtualDeal


class AboutView(TemplateView):
    template_name = 'sites/about.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['version'] = VERSION
        context['version_str'] = '.'.join((str(elem) for elem in VERSION))
        return context


class DonateView(TemplateView):
    template_name = 'sites/donate.html'


class TermsView(TemplateView):
    template_name = 'sites/terms.html'


class ImpressumView(TemplateView):
    template_name = 'sites/impressum.html'


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_home.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            deals = []
            for deal in user.deals:
                deals.append(deal.set_pov(self.request.user))
            context['deals'] = deals
            context['user_feedback_open'] = user.userfeedback_set.filter(
                status=0
                )
            context['push_feedback_open'] = user.pushfeedback_set.filter(
                status=0
                )
            context['lobby'] = Chat.get_lobby()
        else:
            self.template_name = 'dashboard/dashboard_anonymous.html'
        return context


class Ajax2dView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/ajax_2d.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['is_virtual'] = True
        context['deals_2d'] = VirtualDeal.by_users(
            self.request.user,
            self.request.user.other_users
            )
        return context


class Ajax3dView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/ajax_3d.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        return context
