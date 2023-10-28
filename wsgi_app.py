import os
from jinja2 import Environment, FileSystemLoader, Template
from webob import Request, Response

template_path = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)


def render_template(template_name: str, **context) -> dict[Template, str]:
    template = jinja_env.get_template(template_name)
    return {"text": template.render(context), "type": "text/html"}


class Wsgiclass:
    def __init__(self):
        self.dic_rutas = {}

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def ruta(self, path):
        def envoltura(controlador):
            self.dic_rutas[path] = controlador
            return controlador

        return envoltura

    def handle_request(self, request):
        response = Response()

        for path, controlador in self.dic_rutas.items():
            if path == request.path:
                controlador(request, response)
                return response

        self.default_response(response)
        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = "Pagina no encontrada"
