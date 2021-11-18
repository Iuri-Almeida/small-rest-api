class User(object):
    def __init__(self, name: str, age: int, city: str) -> None:
        self.__name = name
        self.__age = age
        self.__city = city

    def __str__(self) -> str:
        return f'Name: {self.__name}, Age: {self.__age}, City: {self.__city}'

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        self.__name = new_name

    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, new_age: int) -> None:
        self.__age = new_age

    @property
    def city(self) -> str:
        return self.__city

    @city.setter
    def city(self, new_city: str) -> None:
        self.__city = new_city
