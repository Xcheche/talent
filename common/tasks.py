from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

def send_email(subject:str,email_to: list[str],html_template,context):
    msg = EmailMultiAlternatives(
        subject=subject,from_email='noreply@example.com',to=email_to
    )
    html_template = get_template(html_template)
    html_content = html_template.render(context)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)