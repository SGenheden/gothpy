import json
import os

from .cloud_util import CloudAddressBookApi


class AddressBook:
    """
    A simple address book class.

    The address book currently stores the name and address of the contacts
    in a dictionary and can save the contacts in an external JSON file.

    It is recommended to use it within a context manager which takes care of
    automatically saving the contacts to disk.

    Examples
    --------
    >>> with AddressBook("autosave.json") as book:
    >>>     book.update("Donald", "Pennsylvania Avenue")

    Parameters
    ----------
    filestore: str, optional
        if given load and save the contacts from/to this file when using a context manager
    """

    def __init__(self, filestore=None):
        self._contacts = {}
        self._filestore = filestore

    def __enter__(self):
        if self._filestore and os.path.exists(self._filestore):
            self.load(self._filestore)
        return self

    def __exit__(self, *args):
        if self._filestore:
            self.save(self._filestore)

    def contact(self, name):
        """
        Return the contact information

        Parameters
        ----------
        name: str
            the name of the contact

        Returns
        -------
        dict:
            the contact information

        Raises
        ------
        KeyError
            if the contact does not exists in the address book
        """
        try:
            return self._contacts[name]
        except KeyError:
            raise KeyError(f"Unknown contact = {name}")

    def delete(self, name):
        """
        Delete the contact from the address book

        Parameters
        ----------
        name: str
            the name of the contact

        Raises
        ------
        KeyError
            if the contact does not exists in the address book
        """
        try:
            del self._contacts[name]
        except KeyError:
            raise KeyError(f"Unknown contact = {name}")

    def load(self, filename):
        """
        Load a JSON file as an address book

        Parameters
        ----------
        filename: str
            the path to JSON file with contacts
        """
        fileobj = open(filename, "r")
        self._contacts = json.load(fileobj)
        fileobj.close()

    def save(self, filename):
        """
        Save the address book to file

        The address book will be stored to in JSON format

        Parameters
        ----------
        filename: str
            the path to a file where the address will be written
        """
        fileobj = open(filename, "w")
        json.dump(self._contacts, fileobj)
        fileobj.close()

    def sync(self, auth):
        """
        Sync the address book with the cloud

        Parameters
        ----------
        auth: str
            the username and password, colon-separated
        """
        api = CloudAddressBookApi("google", auth)
        _dict = api.download()
        self._contacts.update(_dict)
        api.upload(self)

    def to_dict(self):
        """
        Return all contacts stored in the address book

        Returns
        -------
        dict:
            the contacts in the address book
        """
        return self._contacts

    def update(self, name, address):
        """
        Add or update the address of a contact

        Parameters
        ----------
        name: str
            the name of the contact
        address: str
            the address of the contact
        """
        self._contacts[name] = {"address": address}

    def query(self, name):
        """
        Test if a contact exists in the address book

        Parameters
        ----------
        name: str
            the name of the contact
        """
        return name in self._contacts
