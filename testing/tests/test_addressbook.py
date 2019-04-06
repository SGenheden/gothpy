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


def test_save(simple_addressbook, mocker):
    patched_dump = mocker.patch("addressbook.addressbook.json.dumps")
    patched_open = mocker.patch("builtins.open")
    filename = "temp.json"
    simple_addressbook.save(filename)
    patched_open.called_once_with(filename, "w")
    patched_dump.called_once_with(simple_addressbook.to_dict(), patched_open.return_value)
    assert not os.path.exists(filename)


def test_open(simple_addressbook, mocker):
    patched_load = mocker.patch(
        "addressbook.addressbook.json.load", return_value=simple_addressbook.to_dict()
    )
    patched_open = mocker.patch("builtins.open")
    a2 = AddressBook()
    a2.load("temp.json")
    patched_open.called_once_with("temp.json", "r")
    patched_load.called_once_with(patched_open.return_value)
    assert a2.to_dict() == simple_addressbook.to_dict()


def test_sync(simple_addressbook, mocker):
    patched_api = mocker.patch(
        "addressbook.addressbook.CloudAddressBookApi", autospec=True
    )
    patched_api.return_value.download.return_value = {
        "donald": {"address": "pennsylvania avenue"}
    }

    simple_addressbook.sync("usr:pwd")
    patched_api.assert_called_once()
    patched_api.return_value.download.assert_called_once()
    patched_api.return_value.upload.assert_called_once_with(simple_addressbook)
    assert simple_addressbook.query("donald")


def test_sync_failure(simple_addressbook, mocker):
    patched_api = mocker.patch(
        "addressbook.addressbook.CloudAddressBookApi", autospec=True
    )
    patched_api.return_value.download = mocker.MagicMock(
        side_effect=ConnectionError("Unable to connect to API")
    )
    with pytest.raises(ConnectionError):
        simple_addressbook.sync("usr:pwd")


