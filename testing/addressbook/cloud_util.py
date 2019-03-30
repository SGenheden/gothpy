class CloudAddressBookApi:
    """
    A simple API towards a cloud-based address book

    Parameters
    ----------
    service: str
        the cloud service
    auth: str
        the username and password, colon-separated
    """

    def __init__(self, service, auth):
        self._service = service
        self._auth = auth

    def download(self):
        """
        Downloads an address book from the cloud

        Returns
        -------
        dict
            the address book as a dictionary

        Raises
        ------
        ConnectionError
            if unable to connect to the cloud
        """
        return {}

    def upload(self, addressbook_obj):
        """
        Uploads an address book to the cloud

        Parameters
        -------
        addressbook_obj: type
            a class with a to_dict() method that returns the address book as dictionary

        Raises
        ------
        ConnectionError
            if unable to connect to the cloud
        """
        pass
