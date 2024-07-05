import random
import re
import string
import time
from collections.abc import MutableMapping

import requests
from .endpoints import *
from .exceptions import *
from .Mail import Mail as Mailclass
from .Inbox import Inbox as Inboxclass
from .Captcha import Captcha as Captchaclass
from .Search import SearchMail as Searchclass

class Xitroo:
    def __init__(self, mailAddress: str, header: MutableMapping[str, str | bytes] = {}, session: requests.Session = None):
        """
        Xitroo API constructor.
        :param mailAddress: mail address to check for or send mails.
        :param header: optional headers to send with request.
        :param session: optional requests.Session object.
        :type mailAddress: :class:`str`
        :type header: :class:`collections.abc.MutableMapping[str, str | bytes]`
        :type session: :class:`requests.Session`
        """
        self._l: list[str] = ["de", "fr", "com"]
        self._locale: str = mailAddress.strip().split(".")[-1]
        self._header: MutableMapping[str, str | bytes] = header
        self._mailAddress: str = mailAddress.strip()
        self._session: requests.Session = requests.Session() if session is None else session

        if self._locale not in self._l:
            raise InvalidLocale("Error Locale: mailAddress must end with any locale from list: " + ", ".join(self._l) + " (Choosen: " + mailAddress.split('.')[-1] + ")")

        if len(self._header) != 0:
            self._session.headers.update(self._header)


    def getMailAddress(self) -> str:
        """
        Returns the mail address of the current mail address.
        :return: :class:`str`
        """
        return self._mailAddress

    def setMailAddress(self, mailAddress: str) -> None:
        """
        :param mailAddress: Sets the mail address to your given argument.
        :type mailAddress: :class:`str`
        """
        mailAddress: str = mailAddress.strip()
        self._locale: str = mailAddress.split(".")[-1]
        self._mailAddress: str = mailAddress

    def getHeader(self) -> MutableMapping[str, str | bytes]:
        """
        returns the header of the current :class:`requests.Session` instance.
        :return: :class:`collections.abc.MutableMapping[str, str | bytes]`
        """
        return self._header

    def setHeader(self, header: MutableMapping[str, str | bytes]) -> None:
        """
        :param header: sets the header of the current :class:`requests.Session` instance.
        :type header: :class:`collections.abc.MutableMapping[str, str | bytes]`
        """
        self._header: MutableMapping[str, str | bytes] = header
        self._session.headers.update(self._header)

    def getSession(self) -> requests.Session:
        """
        returns the :class:`requests.Session` instance.
        :return: :class:`requests.Session``
        """
        return self._session

    def setSession(self, session: requests.Session) -> None:
        """
        :param session: sets the :class:`requests.Session` instance.
        :type session: :class:`requests.Session``
        """
        self._session: requests.Session = session
        self._header: MutableMapping[str, str | bytes] = self._session.headers



    def equals(self, XitrooObject: __init__) -> bool:
        """
        :param XitrooObject: :class:`Xitroo` Object to compare to.
        :type XitrooObject: :class:`Xitroo`
        :rtype: :class:`bool`
        :return: :class:`bool` - True if equals, false otherwise.
        """
        return self.getMailAddress == XitrooObject.getMailAddress and self.getHeader == XitrooObject.getHeader

    def copy(self) -> __init__:
        """
        Creates a new :class:`Xitroo` instance with a copy of the current :class:`Xitroo` instance.
        :rtype: :class:`Xitroo`
        :return: Copy of :class:`Xitroo` instance
        """
        return self.__class__(self.getMailAddress(), self.getHeader())

    def copyTo(self, XitrooObject: __init__) -> __init__:
        """
        Copy current :class:`Xitroo` instance to given object :class:`Xitroo` instance.
        :param XitrooObject: Already instanced :class:`Xitroo`
        :type XitrooObject: :class:`Xitroo`
        :rtype: :class:`Xitroo`
        :return: Copy of :class:`Xitroo` instance
        """
        raise NotImplementedError()


    def Mail(self, mailId: str) -> Mailclass:
        """
        Create Mail Object to read mail
        :param mailId: Identifier to read mail from.
        :type mailId: :class:`str`
        :rtype: :class:`Mailclass`
        :return: :class:`Mailclass` Object.
        """
        return Mailclass(mailId, self._session, self._locale)

    def Inbox(self, inbox: dict = None) -> Inboxclass:
        """
        Create Inbox Object to read Inbox
        :param inbox: optional Inbox dict if there is one. Should look like this {'totalMails': 0, 'mails': []}.
        :type inbox: :class:`dict`
        :rtype: :class:`Inboxclass`
        :return: :class:`Inboxclass` Object
        """
        return Inboxclass(self._mailAddress, self._session, inbox, self._locale)

    def Captcha(self) -> Captchaclass:
        """
        Create Captcha Object to get or verify captcha
        :rtype: :class:`Captchaclass`
        :return: :class:`Captchaclass` Object
        """
        return Captchaclass(self._session, self._locale)

    # Rewrite Search
    def searchInbox(self) -> Searchclass:
        """
        Create Search Object to search Inbox using :class:`Searchclass`
        :rtype: :class:`Searchclass`
        :return: :class:`Searchclass` Object
        """
        return Searchclass(self._mailAddress, self._session)

    def getRawInbox(self, mailsPerPage=25) -> dict:
        """
        Read current Inbox from ``mailaddress`` to dict
        :param mailsPerPage: optional Number of mails to read from Inbox.
        :type mailsPerPage: :class:`int`
        :rtype: :class:`dict`
        :return: :class:`dict` of Inbox
        """
        return self.Inbox().getRawInbox(mailsPerPage)

    def getRawMail(self, mailId: str) -> dict:
        """
        Read current Mail from ``mailId`` to dict
        :param mailId: Identifier to read mail from.
        :type mailId: :class:`str`
        :rtype: :class:`dict`
        :return: :class:`dict` of Mail
        """
        return self.Mail(mailId).getRawMail()


    def _verifyCaptchaAsUserInput(self) -> str:
        captchaid: str = ""
        solution: str = ""
        r = {"authSuccess": False}
        while not r["authSuccess"]:
            reload: bool = True
            params: dict[str, str] = {"locale": self._locale}
            while reload:
                r: dict = self._session.get(GETCAPTCHA, headers=self._header, params=params).json()
                captchaid: str = r["authID"]
                captcha: str = r["captchaCode"]
                print(captcha)
                solution: str = input("Solve Captcha (r for reload, e for exit): ")
                if solution != "r":
                    reload = False
                if solution == "e":
                    return ""
            params.update({
                "authID": captchaid,
                "captchaSolution": solution
            })
            r: dict = self._session.get(SENDCAPTCHA, headers=self._header, params=params).json()
            if not r["authSuccess"]:
                print("Captcha failed")
        return captchaid

    def sendMail(self, recipient: str, subject: str, Text: str, mode: int = 1, id: str = "") -> bool:
        """
        Send Mail as given ``mailaddress`` in constructor to ``recipient`` with given ``subject`` and ``Text``.
        :param recipient: recipient email address.
        :type recipient: :class:`str`
        :param subject: subject to send with.
        :type subject: :class:`str`
        :param Text: text to send.
        :type Text: :class:`str`
        :param mode: optional send mode. - **1**: manual userinput to get captcha id; **0**: no userinput, but requires captcha id. Create captcha id with ``Xitroo.Captcha`` :class:`Captchaclass`.
        :type mode: :class:`int`
        :param id: optional captcha id which is required to send mail if mode 0 is selected.
        :type id: :class:`str`
        :rtype: :class:`bool`
        :return: :class:`bool` - True if sent successfully, false otherwise.
        """
        if mode:
            id: str = self._verifyCaptchaAsUserInput()
        params: dict[str, str] = {"locale": self._locale}
        if not id:
            return False
        data: dict[str, str] = {
            "authID": id,
            "bodyText": Text,
            "from": self._mailAddress,
            "recipient": recipient,
            "replyMailID": "",
            "subject": subject
        }
        r: requests.Response = self._session.post(SENDMAIL, headers=self._header, params=params, data=data)
        if r.status_code != 200:
            return False
        return True

    @staticmethod
    def generate(prefix: str = "", suffix: str = "", locale: str = "de", randomletterscount: int = 10) -> str:
        """
        Static Method to Generate random email String of given ``length``, ``prefix``, ``suffix`` and ``locale``.
        :param prefix: optional prefix to generate email String.
        :type prefix: :class:`str`
        :param suffix: optional suffix to generate email String.
        :type suffix: :class:`str`
        :param locale: optional locale to generate domain of email string. [de, fr, com] only are **supported**.
        :type locale: :class:`str`
        :param randomletterscount: optional number of random letters to generate into email String.
        :type randomletterscount: :class:`int`
        :rtype: :class:`str`
        :return: email String.
        """
        return prefix + "".join(random.choices(string.ascii_letters, k=randomletterscount)) + suffix + "@xitroo." + locale

    @staticmethod
    def getCode(body: str, codelength: int = 6) -> str:
        """
        Static Method to get code from given ``body`` and ``codelength`` to identify the code.
        :param body: bodytext of email.
        :param codelength: optional length of code to parse. Default is 6.
        :type body: :class:`str`
        :type codelength: :class:`int`
        :rtype: :class:`str`
        :return: Verification Code.
        """
        return re.search('\\d{' + str(codelength) + '}', body).group(0)

    def getLatestMail(self) -> Mailclass | None:
        """
        Get latest Mail from ``mailaddress``
        :rtype: :class:`Mailclass` | None
        :return: :class:`Mailclass` Object of latest Mail or None if no latest Mail is found.
        """
        if self.Inbox().getTotalMails() != 0:
            return self.Inbox().getMailFirst()
        return None

    def waitForLatestMail(self, maxTime=60, sleepTime=5, checkMail=100) -> Mailclass:
        """
        Wait until latest Mail.
        :param maxTime: optional maximum time of the difference between current time and latest Mail received mail time to get only new mail.
        :param sleepTime: optional sleep time in seconds between checking latest mail.
        :param checkMail: optional Interval to check if latest Mail is found.
        :type maxTime: :class:`int`
        :type sleepTime: :class:`int`
        :type checkMail: :class:`int`
        :rtype: :class:`Mailclass`
        :return: :class:`Mailclass` Object of latest Mail.
        """
        for i in range(checkMail):
            latest = self.getLatestMail()
            if latest:
                if not(latest.getRawMail()["arrivalTimestamp"] + maxTime < time.time()):
                    return latest
            print("Waiting for latest mail...")
            time.sleep(sleepTime)
