from rest_framework.renderers import JSONRenderer
import json


class ResponseJSONRenderer(JSONRenderer):
    """Преобразование ответа"""
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get('errors', None)

        if errors is not None:
            return super(ResponseJSONRenderer, self).render(data)

        return json.dumps({
            'data': data
            })
