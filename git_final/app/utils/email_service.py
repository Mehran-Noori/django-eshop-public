from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_email(subject, to, context, template_name):
    try:
        print("do")

        html_message = render_to_string(template_name, context)
        print("do1")
        plain_message = strip_tags(html_message)
        print("do2")

        from_email = settings.EMAIL_HOST_USER

        send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    except:
        # todo: add log system later?
        print("fail")

