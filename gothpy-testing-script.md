
# introduction (10)
- kodcentrum
- survey
- pytest

- application

show API docs

show some example usage of the application

# part 1 - assertions (5)

## simple assertion

create tests **package**

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

## assertion with exception

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

# part 2 - fixtures

### built-in fixture: tempfolder (5)

    def test_save_load(tmpdir):
        filename = tmpdir.join("temp.json")
        a1 = AddressBook()
        a1.update("harry", "4 Privet Drive")
        a1.save(filename)
        assert os.path.exists(filename)

        a2 = AddressBook()
        a2.load(filename)
        assert a2.to_dict() == a1.to_dict()

### custom fixture (10)

** simple**

    @pytest.fixture
    def simple_addressbook():
        a = AddressBook()
        a.update("harry", "4 Privet Drive")
        a.update("bruce", "wayne manor")
        return a

replace functions

    def test_update2(simple_addressbook):
        assert simple_addressbook.contact("harry") == {"address": "4 Privet Drive"

    def test_query2(simple_addressbook):
        a = simple_addressbook
        assert a.query("harry")
        assert not a.query("dr holmes")

    def test_delete2(simple_addressbook):
        a = simple_addressbook
        a.delete("harry")
        assert not a.query("harry")


### external fixture: datadir (5)

* Create example.json in *data* folder


    @pytest.fixture
    def autosave_addressbook(shared_datadir):
        filename = str(shared_datadir / "example.json")
        a  = AddressBook()
        a.load(filename)
        yield a
        a.save(filename)
        os.remove(filename)

    @pytest.fixture
    def autosave_addressbook(shared_datadir):
        filename = str(shared_datadir / "example.json")
        with AddressBook(filename) as a:
            yield a

* Explain yield here
* Show the data folder in $TMP
* Show how it is modified by delete


    def test_delete3(autosave_addressbook):
        a = autosave_addressbook
        a.delete("harry")
        assert not a.query("harry")

# part 3 - mocking (15)

Talk about the cloud API

Start with printing out type information

    def test_sync(simple_addressbook, mocker):
        import addressbook.addressbook
        print(f"\nType of cloud adress book = {type(addressbook.addressbook.CloudAddressBookApi)}")
        patched_api = mocker.patch(
            "addressbook.addressbook.CloudAddressBookApi", autospec=True
        )
        print(f"Type of cloud adress book = {type(addressbook.addressbook.CloudAddressBookApi)}")

        import addressbook.cloud_util
        print(f"Type of cloud adress book = {type(addressbook.cloud_util.CloudAddressBookApi)}")
        print(dir(addressbook.addressbook.CloudAddressBookApi))

    pytest -vs tests/test_addressbook.py::test_sync2

Discuss what magic mock object is

    def test_sync(simple_addressbook, mocker):
        patched_api = mocker.patch(
            "addressbook.addressbook.CloudAddressBookApi", autospec=True
        )
        # patched_api.return_value.download.return_value = {
            "donald": {"address": "pennsylvania avenue"}
        }

        simple_addressbook.sync("usr:pwd")
        patched_api.assert_called_once()
        patched_api.return_value.download.assert_called_once()
        patched_api.return_value.upload.assert_called_once_with(simple_addressbook)
        # assert simple_addressbook.query("donald")

Side effect

    def test_sync_failure(simple_addressbook, mocker):
        patched_api = mocker.patch(
            "addressbook.addressbook.CloudAddressBookApi", autospec=True
        )
        patched_api.return_value.download = mocker.MagicMock(
            side_effect=ConnectionError("Unable to connect to API")
        )
        with pytest.raises(ConnectionError):
            simple_addressbook.sync("usr:pwd")

# part 4 -misc

## marks

- skip

- custom mark


    @pytest.mark.external
    def test_save_load(tmpdir):
        filename = tmpdir.join("temp.json")
        a1 = AddressBook()
        a1.update("harry", "4 Privet Drive")
        a1.save(filename)
        assert os.path.exists(filename)

        a2 = AddressBook()
        a2.load(filename)
        assert a2.to_dict() == a1.to_dict()

    pytest -m external
    pytest -m "not external"

## plugins (5)

- coverage


    pytest --cov addressbook
    pytest --cov addressbook  --cov-report html


- html


    pytest --html report.html

- random


    pytest --random
