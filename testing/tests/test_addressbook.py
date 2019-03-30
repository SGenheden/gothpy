import pytest
from addressbook.addressbook import AddressBook


def test_update():
    a = AddressBook()
    a.update("harry", "4 Privet Drive")
    assert a.contact("harry") == {"address": "4 Privet Drive"}


def test_query():
    a = AddressBook()
    a.update("harry", "4 Privet Drive")
    assert a.query("harry")
    assert not a.query("dr holmes")


def test_delete():
    a = AddressBook()
    a.update("harry", "4 Privet Drive")
    a.delete("harry")
    assert not a.query("harry")


def test_get_none_existing():
    a = AddressBook()
    with pytest.raises(KeyError) as excinfo:
        a.contact("harry")
    assert "harry" in str(excinfo.value)


def test_delete_non_existing():
    a = AddressBook()
    with pytest.raises(KeyError) as excinfo:
        a.delete("harry")
    assert "harry" in str(excinfo.value)
