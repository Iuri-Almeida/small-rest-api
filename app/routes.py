def render_template(template: str = 'index.html', context: dict = None) -> str:

    with open(f'app/pages/{template}', 'r') as file:
        html = file.read()
        html = html.format(**context or {})

    return html


def home(context: dict = None) -> str:
    return render_template('index.html', context or {})


def not_found(context: dict = None) -> str:
    return render_template('404.html', context or {})
