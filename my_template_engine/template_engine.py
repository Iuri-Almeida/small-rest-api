from re import split, match

from my_template_engine.code_builder import CodeBuilder
from my_template_engine.template_engine_error import TemplateEngineSyntaxError


class TemplateEngine(object):

    def __init__(self, txt: str, *contexts: dict) -> None:
        self.__context = {}
        for context in contexts:
            self.__context.update(context)

        self.__all_vars = set()
        self.__loop_vars = set()

        code = CodeBuilder()

        code.add_line('def render_function(context: dict, do_dots: callable) -> str:')
        code.indent()
        vars_code = code.add_section()
        code.add_line('result = []')
        code.add_line('append_result = result.append')
        code.add_line('extend_result = result.extend')
        code.add_line('to_str = str')

        tag_stack = []
        structure_stack = []

        def put_tags_into_code() -> None:
            if len(tag_stack) == 1:
                code.add_line(f'append_result({tag_stack[0]})')
            elif len(tag_stack) > 1:
                code.add_line(f'extend_result([{", ".join(tag_stack)}])')
            del tag_stack[:]

        tags = split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", txt)
        for tag in tags:
            # Comment
            if tag.startswith('{#'):
                continue

            # Variable
            elif tag.startswith('{{'):
                expr = self.__expr_code(tag[2:-2].strip())
                tag_stack.append(f'to_str({expr})')

            # Structures: if, for
            elif tag.startswith('{%'):
                put_tags_into_code()

                words = tag[2:-2].strip().split()

                # if statement
                if words[0] == 'if':
                    if len(words) != 2:
                        raise TemplateEngineSyntaxError(f'Do not understand if statement: {repr(tag)}')

                    structure_stack.append('if')

                    code.add_line(f'if {self.__expr_code(words[1])}:')
                    code.indent()

                # for statement
                elif words[0] == 'for':
                    if len(words) != 4 or words[2] != 'in':
                        raise TemplateEngineSyntaxError(f'Do not understand for statement: {repr(tag)}')

                    structure_stack.append('for')

                    self.__variable(words[1], self.__loop_vars)

                    code.add_line(f'for c_{words[1]} in {self.__expr_code(words[3])}:')
                    code.indent()

                # closing statements (if, for)
                elif words[0].startswith('end'):
                    if len(words) != 1:
                        raise TemplateEngineSyntaxError(f'Do not understand end statement: {repr(tag)}')

                    if not structure_stack:
                        raise TemplateEngineSyntaxError(f'There are too many ends: {repr(tag)}')

                    start_statement = structure_stack.pop()
                    end_statement = words[0][3:]

                    if start_statement != end_statement:
                        raise TemplateEngineSyntaxError(f'Mismatched end tag: {repr(end_statement)}')

                    code.dedent()

                # different tag
                else:
                    raise TemplateEngineSyntaxError(f'Do not understand tag: {repr(words[0])}')

            # text
            else:
                if tag:
                    tag_stack.append(repr(tag))

        # still an open structure
        if structure_stack:
            raise TemplateEngineSyntaxError(f'Unmatched action tag: {repr(structure_stack[-1])}')

        put_tags_into_code()

        # adding our custom variables
        for var_name in (self.__all_vars - self.__loop_vars):
            vars_code.add_line(f'c_{var_name} = context[{repr(var_name)}]')

        code.add_line('return "".join(result)')
        code.dedent()

        self.__render_function = code.get_globals()['render_function']

    def __expr_code(self, expr: str) -> str:
        # function
        if '::' in expr:
            pipes = expr.split('::')
            code = self.__expr_code(pipes[0])

            for func in pipes[1:]:
                self.__variable(func, self.__all_vars)
                code = f'c_{func}({code})'

        # object
        elif '.' in expr:
            dots = expr.split('.')
            code = self.__expr_code(dots[0])
            args = ', '.join(repr(d) for d in dots[1:])
            code = f'do_dots({code}, {args})'

        # variable
        else:
            self.__variable(expr, self.__all_vars)
            code = f'c_{expr}'

        return code

    @staticmethod
    def __variable(name: str, vars_set: set) -> None:
        if not match(r"[_a-zA-Z][_a-zA-Z0-9]*$", name):
            raise TemplateEngineSyntaxError(f'Not a valid name: {repr(name)}')
        vars_set.add(name)

    def render(self, context: dict = None) -> str:
        render_context = dict(self.__context)

        if context:
            render_context.update(context)

        return self.__render_function(render_context, self.__do_dots)

    @staticmethod
    def __do_dots(value, *dots):
        for dot in dots:
            try:
                value = getattr(value, dot)
            except AttributeError:
                value = value[dot]

            if callable(value):
                value = value()

        return value
