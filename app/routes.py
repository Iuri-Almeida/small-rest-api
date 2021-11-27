from my_template_engine.template_engine import TemplateEngine


def render_template(template: str = 'index.html', context: dict = None) -> str:

    with open(f'app/pages/{template}', 'r') as file:
        engine = TemplateEngine(file.read())
        html = engine.render(context or {})

    return html


def home(context: dict = None) -> str:
    return render_template('index.html', context or {})


def not_found(context: dict = None) -> str:
    return render_template('404.html', context or {})
