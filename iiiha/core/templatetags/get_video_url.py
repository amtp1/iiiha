from django.template import Library

import fal_client

register = Library()


def get_video_url(request_id):
    try:
        result = fal_client.result("fal-ai/luma-dream-machine", request_id)
        return result['video']['url']
    except Exception as e:
        return str(e)


register.filter('get_video_url', get_video_url)
