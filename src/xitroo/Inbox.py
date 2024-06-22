import time
import requests
from .exceptions import EmailNotFound, GETRequestException
from .endpoints import *
from .Mail import Mail as Mailclass
class Inbox:
    def __init__(self, mailAddress: str = None,
                 session: requests.Session = requests.Session(),
                 inbox: dict = None,
                 locale: str = "com"):
        """
        Inbox constructor.
        :param mailAddress: Mail address required if inbox is None
        :param session: optional :class:`requests.Session`
        :param inbox: optional dict of Inbox.
        :param locale: optional locale to use for inbox.
        :type inbox: :class:`dict`
        :type locale: :class:`str`
        :type session: :class:`requests.Session`
        :type mailAddress: :class:`str`
        """
        self._session: requests.Session = session
        self._locale: str = locale.strip()

        if mailAddress is None and inbox is None:
            raise ValueError("Either mailAddress or inbox must be specified.")

        self._mailAddress: str = mailAddress.strip() if mailAddress else None
        self._inbox: dict = inbox if inbox is not None else self.getRawInbox()

    def getRawInbox(self, mailsPerPage=25) -> dict:
        """
        Get raw Inbox.
        :param mailsPerPage: number of mails to fetch.
        :type mailsPerPage: :class:`int`
        :rtype: :class:`dict`
        :return: :class:`dict` of inbox
        """
        params: dict[str, str] = {
            "locale": self._locale,
            "mailAddress": self._mailAddress,
            "mailsPerPage": mailsPerPage,
            "minTimestamp": "0",
            "maxTimestamp": time.time()
        }
        reqeust: requests.Response = self._session.get(MAILS, params=params)
        if reqeust.status_code != 200:
            raise GETRequestException("raw Inbox", reqeust.text, reqeust.status_code)
        content: dict = reqeust.json()
        # Translate for later usage #1
        if "type" in content:
            return {'totalMails': 0, 'mails': []}
        return content

    def getTotalMails(self) -> int:
        """
        Get total number of mails in ``Inbox``.
        :rtype: :class:`int`
        :return: :class:`int`
        """
        return self._inbox['totalMails']

    def getRawMails(self) -> dict:
        """
        Get raw mails in ``Inbox``.
        :rtype: :class:`dict`
        :return: :class:`dict`
        """
        return self._inbox['mails']

    def getRawMail(self, index: int) -> dict:
        """
        Get raw mail in ``Inbox`` by index.
        :param index: index of mail to fetch.
        :type index: :class:`int`
        :rtype: :class:`dict`
        :return: :class:`dict`
        """
        total = self.getTotalMails()
        if total*-1 <= index < total and total > 0:
            return self._inbox['mails'][index]
        else:
            if total == 0:
                raise EmailNotFound(f"Inbox from {self._mailAddress} does not contain any mail.")
            raise EmailNotFound("Index out of range for Inbox from {self._mailAddress}")

    def getMail(self, index: int) -> Mailclass:
        """
        Get :class:`Mailclass` object in ``Inbox`` by index.
        :param index: index of mail to fetch.
        :type index: :class:`int`
        :rtype: :class:`Mailclass`
        :return: :class:`Mailclass`
        """
        return Mailclass(self.getRawMail(index)["_id"], self._session)

    def getMailFirst(self) -> Mailclass:
        """
        Get first mail in ``Inbox``.
        :rtype: :class:`Mailclass`
        :return: :class:`Mailclass`
        """
        return Mailclass(self.getRawMail(0)["_id"], self._session)

    def getMailLast(self) -> Mailclass:
        """
        Get last mail in ``Inbox``.
        :rtype: :class:`Mailclass`
        :return: :class:`Mailclass`
        """
        return Mailclass(self.getRawMail(-1)["_id"], self._session)
