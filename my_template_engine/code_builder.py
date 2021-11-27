class CodeBuilder(object):

    __INDENT_STEP = 4

    def __init__(self, indent: int = 0) -> None:
        self.__indent_level = indent
        self.__code = []

    def __str__(self) -> str:
        return ''.join(str(i) for i in self.__code)

    def add_line(self, new_line: str) -> None:
        self.__code.extend([' ' * self.__indent_level, new_line, '\n'])

    def indent(self) -> None:
        self.__indent_level += self.__INDENT_STEP

    def dedent(self) -> None:
        self.__indent_level -= self.__INDENT_STEP

    def add_section(self):
        section: CodeBuilder = CodeBuilder(self.__indent_level)
        self.__code.append(section)

        return section

    def get_globals(self) -> dict:
        assert self.__indent_level == 0

        source_code = str(self)

        namespaces = {}
        exec(source_code, namespaces)

        return namespaces
