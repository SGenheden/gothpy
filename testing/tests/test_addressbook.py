import os
import pytest
from addressbook.addressbook import AddressBook


def test_update(simple_addressbook):
    assert len(simple_addressbook.to_dict()) == 1
    assert "harry" in simple_addressbook.to_dict()


def test_contact(simple_addressbook):
    contact = simple_addressbook.contact("harry")
    assert contact == {"address": "4 Privet Drive"}


def test_query(simple_addressbook):
    assert simple_addressbook.query("harry")
    assert not simple_addressbook.query("dr holmes")


def test_delete(simple_addressbook):
    simple_addressbook.delete("harry")
    assert len(simple_addressbook.to_dict()) == 0


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


def test_save_load(simple_addressbook, tmpdir):
    filename = tmpdir.join("temp.json")
    a1 = simple_addressbook
    a1.save(filename)
    assert os.path.exists(filename)

    a2 = AddressBook()
    a2.load(filename)
    assert a2.to_dict() == a1.to_dict()


def test_load(simple_addressbook, shared_datadir):
    filename = str(shared_datadir / "example.json")
    simple_addressbook.load(filename)
    assert len(simple_addressbook.to_dict()) == 3
