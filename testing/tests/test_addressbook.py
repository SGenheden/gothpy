import os
import pytest
from addressbook.addressbook import AddressBook


def test_update1(simple_addressbook):
    assert simple_addressbook.contact("harry") == {"address": "4 Privet Drive"}


def test_update2(autosave_addressbook):
    assert autosave_addressbook.contact("harry") == {"address": "4 Privet Drive"}
    assert autosave_addressbook.contact("clark") == {"address": "1938 Sulivan Ln"}


def test_query(simple_addressbook):
    a = simple_addressbook
    assert a.query("harry")
    assert not a.query("dr holmes")


def test_delete(simple_addressbook):
    a = simple_addressbook
    a.delete("harry")
    assert not a.query("harry")


def test_delete2(autosave_addressbook):
    a = autosave_addressbook
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


def test_save_load(simple_addressbook, tmpdir):
    filename = tmpdir.join("temp.json")
    a1 = simple_addressbook
    a1.save(filename)
    assert os.path.exists(filename)

    a2 = AddressBook()
    a2.load(filename)
    assert a2.to_dict() == a1.to_dict()
