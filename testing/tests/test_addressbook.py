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


def test_save(simple_addressbook, mocker):
    patched_dump = mocker.patch("addressbook.addressbook.json.dumps")
    fileobj = mocker.MagicMock()
    patched_open = mocker.patch("builtins.open", return_value=fileobj)
    filename = "temp.json"
    simple_addressbook.save(filename)
    patched_open.called_once_with(filename, "w")
    patched_dump.called_once_with(simple_addressbook.to_dict(), fileobj)
    assert not os.path.exists(filename)


def test_open(simple_addressbook, mocker):
    patched_load = mocker.patch(
        "addressbook.addressbook.json.load", return_value=simple_addressbook.to_dict()
    )
    fileobj = mocker.MagicMock()
    patched_open = mocker.patch("builtins.open", return_value=fileobj)
    a2 = AddressBook()
    a2.load("temp.json")
    patched_open.called_once_with("temp.json", "r")
    patched_load.called_once_with(fileobj)
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
