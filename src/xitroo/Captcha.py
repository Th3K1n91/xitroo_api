import requests
from .endpoints import *
from .exceptions import CaptchaException
class Captcha:
    def __init__(self, session: requests.Session = requests.Session(), locale: str = "com"):
        """
        Captcha constructor.
        :param session: optional :class:`requests.Session`
        :param locale: optional locale. Default is "com"
        :type locale: class:`str`
        :type session: :class:`requests.Session`
        """
        self._session: requests.Session = session
        self._locale: str = locale
        self.id: str = ""

    def getCaptcha(self) -> dict:
        """
        Get captcha data as dict.
        :return: :class:`dict`
        """
        params: dict[str, str] = {"locale": self._locale}
        r: dict = self._session.get(GETCAPTCHA, params=params).json()
        self.id: str = r["authID"]
        return r

    def verifyCaptcha(self, solution: str, id: str = "") -> bool:
        """
        Verify the captcha by checking if the solution is correct.
        :param solution: Captcha solution.
        :param id: optional Captcha id if creating a new Captcha object.
        :type solution: :class:`str`
        :type id: :class:`str`
        :rtype: :class:`bool`
        :return: :class:`bool` indicating if the solution is correct.
        """
        if self.id is None and id:
            self.id: str = id
        if not self.id and not id:
            raise CaptchaException("Create Captcha Object or pass in a captcha id")
        params: dict[str, str] = {"locale": self._locale,
                                  "authID": self.id,
                                  "captchaSolution": solution
                                  }
        r: dict = self._session.get(SENDCAPTCHA, params=params).json()
        if not r["authSuccess"]:
            return False
        return True
