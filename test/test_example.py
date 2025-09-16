import pytest


def test_equal_or_not_equal():
    assert 1 == 1
    assert 1 != 2


def test_is_instance():
    assert isinstance(1, int)
    assert not isinstance(1, str)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_student():
    return Student("John", "Doe", "Mathematics", 2)


def test_person_initialization(default_student):
    assert default_student.first_name == "John"
    assert default_student.last_name == "Doe"
    assert default_student.major == "Mathematics"
    assert default_student.years == 2
