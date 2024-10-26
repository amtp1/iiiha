from django.template import Library

import fal_client

register = Library()


def get_video_url(request_id):
    result = fal_client.result("fal-ai/kling-video/v1/standard/text-to-video", request_id)
    return result['video']['url']


register.filter('get_video_url', get_video_url)
