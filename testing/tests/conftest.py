import pytest
from addressbook.addressbook import AddressBook


@pytest.fixture
def simple_addressbook():
    a = AddressBook()
    a.update("harry", "4 Privet Drive")
    return a


@pytest.fixture
def loaded_addressbook(shared_datadir):
    filename = str(shared_datadir / "example.json")
    with AddressBook(filename) as a:
        yield a
