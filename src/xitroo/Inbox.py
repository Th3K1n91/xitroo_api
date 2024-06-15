import time
from .Mail import Mail as Mailclass
class Inbox:
    def __init__(self, xitroo, inbox: dict = None):
        """
        Inbox constructor.
        :param xitroo: Xitroo object.
        :param inbox: optional dict of Inbox.
        :type inbox: :class:`dict`
        :type xitroo: :class:`xitroo.Xitroo.Xitroo`
        """
        self._xitroo = xitroo
        if inbox == "":
            self._inbox: dict = inbox
        else:
            self._inbox: dict = self.getRawInbox()

    def getRawInbox(self, mailsPerPage=25) -> dict:
        """
        Get raw Inbox.
        :param mailsPerPage: number of mails to fetch.
        :type mailsPerPage: :class:`int`
        :rtype: :class:`dict`
        :return: :class:`dict` of inbox
        """
        params: dict[str, str] = {
            "locale": self._xitroo._locale,
            "mailAddress": self._xitroo._mailAddress,
            "mailsPerPage": mailsPerPage,
            "minTimestamp": "0",
            "maxTimestamp": time.time()
        }
        reqeust: dict = self._xitroo._session.get(self._xitroo._MAILS, params=params).json()
        # Translate for later usage #1
        if "type" in reqeust:
            return {'totalMails': 0, 'mails': []}
        return reqeust

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
        if not index < 0 or not index >= self.getTotalMails():
            return self._inbox['mails'][index]

    def getMail(self, index: int) -> Mailclass:
        """
        Get :class:`Mailclass` object in ``Inbox`` by index.
        :param index: index of mail to fetch.
        :type index: :class:`int`
        :rtype: :class:`Mailclass`
        :return: :class:`Mailclass`
        """
        return self._xitroo.Mail(self.getRawMail(index)["_id"])

    def getMailFirst(self) -> Mailclass:
        """
        Get first mail in ``Inbox``.
        :rtype: :class:`Mailclass`
        :return: :class:`Mailclass`
        """
        return self._xitroo.Mail(self.getRawMail(0)["_id"])

    def getMailLast(self) -> Mailclass:
        """
        Get last mail in ``Inbox``.
        :rtype: :class:`Mailclass`
        :return: :class:`Mailclass`
        """
        return self._xitroo.Mail(self.getRawMail(-1)["_id"])


    # def searchRegex(self):
    #     return self._xitroo.searchInboxRegex()
