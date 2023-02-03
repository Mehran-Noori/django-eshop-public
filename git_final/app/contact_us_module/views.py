from django.shortcuts import render
from .forms import ContactUsModelForm
from django.views.generic.edit import CreateView
from site_module.models import SiteSetting
from .models import ContactUs


# Create your views here.
class ContactUsView(CreateView):
    form_class = ContactUsModelForm
    template_name = 'contact_us_module/contact_us.html'
    success_url = '/contact-us/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting

        return context
