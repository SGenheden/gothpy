import pytest
from addressbook.addressbook import AddressBook


@pytest.fixture
def simple_addressbook():
    a = AddressBook()
    a.update("harry", "4 Privet Drive")
    a.update("bruce", "wayne manor")
    return a


@pytest.fixture
def autosave_addressbook(shared_datadir):
    filename = str(shared_datadir / "example.json")
    with AddressBook(filename) as a:
        yield a
