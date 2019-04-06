import pytest
from addressbook.addressbook import AddressBook


def test_update():
    a = AddressBook()
    a.update("harry", "4 Privet Drive")
    assert len(a.to_dict()) == 1
    assert "harry" in a.to_dict()


def test_contact():
    a = AddressBook()
    a.update("harry", "4 Privet Drive")
    contact = a.contact("harry")
    assert contact == {"address": "4 Privet Drive"}


def test_query():
    a = AddressBook()
    a.update("harry", "4 Privet Drive")
    assert a.query("harry")
    assert not a.query("dr holmes")


def test_delete():
    a = AddressBook()
    a.update("harry", "4 Privet Drive")
    a.delete("harry")
    assert len(a.to_dict()) == 0


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
