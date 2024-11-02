from django.template import Library

import fal_client

register = Library()


def check_status(request_id):
    status = fal_client.status("fal-ai/luma-dream-machine", request_id, with_logs=True)
    if isinstance(status, fal_client.InProgress):
        return "В процессе"
    elif isinstance(status, fal_client.Queued):
        return "В очереди"
    elif isinstance(status, fal_client.Completed):
        return "Готово"


register.filter('check_status', check_status)
