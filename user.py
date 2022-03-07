import uuid


class User:
    def __init__(self, name):
        self.uid = uuid.uuid4()
        self.name = name


if __name__ == '__main__':
    import pytest
    pytest.main()

