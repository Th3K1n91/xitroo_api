import base64
import requests
import os
import re
from .endpoints import *

class Mail:
    def __init__(self, mailId: str,
                 session: requests.Session = requests.Session(),
                 locale: str = 'com'):
        """
        Mail constructor
        :param mailId: Mail id to identify mail to read.
        :param session: optional :class:`requests.Session` object.
        :param locale: optional locale to identify mail to.
        :type mailId: :class:`str`
        :type session: :class:`requests.Session`
        :type locale: :class:`str`
        """
        self._locale: str = locale.strip()
        self._session: requests.Session = session
        self._mailId: str = mailId.strip()

    def getBodyHtml(self) -> str:
        """
        Get body html content of ``mailId``.
        :rtype: :class:`str`
        :return: :class:`str`
        """
        return base64.b64decode(self.getRawMail()['bodyHtml']).decode('utf-8')

    def getBodyHtmlStrict(self) -> str:
        """
        Get strict body html content of ``mailId``.
        :rtype: :class:`str`
        :return: :class:`str`
        """
        return base64.b64decode(self.getRawMail()['bodyHtmlStrict']).decode('utf-8')

    def getBodyText(self) -> str:
        """
        Get text content of ``mailId``.
        :rtype: :class:`str`
        :return: :class:`str`
        """
        return base64.b64decode(self.getRawMail()['bodyText']).decode('utf-8')

    def getContentType(self) -> str:
        """
        Get content type of ``mailId``.
        :rtype: :class:`str`
        :return: :class:`str`
        """
        return self.getRawMail()['contentType']

    def getExpiration(self) -> float:
        """
        Get expiration timestamp of ``mailId``.
        :rtype: :class:`float`
        :return: :class:`float`
        """
        return self.getRawMail()['expireTimestamp']

    def getFromMail(self) -> str:
        """
        Get mail sender from ``mailId``.
        :rtype: :class:`str`
        :return: :class:`str`
        """
        return self.getRawMail()['from']

    def getRawHeader(self) -> str:
        """
        Get raw header content of ``mailId``.
        :rtype: :class:`str`
        :return: :class:`str`
        """
        return self.getRawMail()['rawHeader']

    def getArrivalTimestamp(self) -> float:
        """
        Get arrival timestamp of ``mailId``.
        :rtype: :class:`float`
        :return: :class:`str`
        """
        return self.getRawMail()['arrivalTimestamp']

    def compareTimeTo(self, Mailobj: __init__) -> float:
        """
        Compare timestamp of ``self`` to ``Mailobj``.
        :param Mailobj: Another Mail object to compare.
        :type Mailobj: :class:`Mail`
        :rtype: :class:`float`
        :return: :class:`float` value between ``self`` and ``Mailobj``.
        """
        return self.getArrivalTimestamp() - Mailobj.getArrivalTimestamp()

    def getSubject(self) -> str:
        """
        Get subject of ``mailId``.
        :rtype: :class:`str`
        :return: :class:`str`
        """
        return base64.b64decode(self.getRawMail()['subject']).decode('utf-8')

    def getAttachments(self) -> list:
        """
        Get attachments of ``mailId``.
        :rtype: :class:`list`
        :return: :class:`list`
        """
        return self.getRawMail()['attachments']

    def downloadAttachment(self, filetodownload: str, path: str = None) -> bool:
        """
        Download attachments of ``mailId`` to ``path``.
        :param filetodownload: Attachment to download.
        :param path: Path where to save the downloaded file.
        :type filetodownload: :class:`str`
        :type path: :class:`str`
        :return: :class:`bool` indicating success or failure.
        """
        fpath = filetodownload if path is None else os.path.join(path, filetodownload)
        if os.path.exists(fpath):
            return False
        params: dict[str, str] = {
            "locale": self._locale,
            "filename": filetodownload,
            "id": self._mailId,
        }
        r: requests.Response = self._session.get(ATTACHMENT, params=params)
        if r.status_code != 200:
            return False
        data = r.json()["data"]
        with open(fpath, 'wb') as f:
            f.write(base64.b64decode(data))
            f.close()
        return True

    def readAttachment(self, filetoread: str, encoding: str = 'utf-8') -> str:
        """
        Read attachment of ``filetoread`` in ``mailId`` to desired ``encoding``.
        :param filetoread: Attachment to read.
        :param encoding: Encoding to use when reading the attachment.
        :type filetoread: :class:`str`
        :type encoding: :class:`str`
        :rtype: :class:`str`
        :return: :class:`str`
        """
        params: dict[str, str] = {
            "locale": self._locale,
            "filename": filetoread,
            "id": self._mailId,
        }
        r: requests.Response = self._session.get(ATTACHMENT, params=params)
        if r.status_code != 200:
            return "Error reading attachment"
        return base64.b64decode(r.json()["data"]).decode(encoding)

    def delete(self) -> bool:
        """
        Delete ``mailId`` from inbox.
        :rtype: :class:`bool`
        :return: :class:`bool` if successful or not.
        """
        params = {
            "locale": self._locale,
            "id": self._mailId
        }
        r: requests.Response = self._session.get(DELETE, params=params)
        if r.status_code != 200:
            return False
        return True

    def reply(self, text: str) -> bool:
        """
        Reply to ``mailId``.
        :param text: Text to reply.
        :type text: :class:`str`
        :rtype: :class:`bool`
        :return: :class:`bool` if successful or not.
        """
        raise NotImplementedError()

    def getCode(self, codelength: int = 6) -> str:
        """
        Static Method to get code from ``mailId`` with ``codelength`` to identify the code.
        :param codelength: optional length of code to parse. Default is 6.
        :type codelength: :class:`int`
        :rtype: :class:`str`
        :return: Verification Code.
        """
        return re.search('\\d{' + str(codelength) + '}', self.getBodyText()).group(0)

    def getRawMail(self) -> dict:
        """
        Get raw mail content of ``mailId``.
        :rtype: :class:`dict`
        :return: :class:`dict` of ``mailId``
        """
        params: dict[str, str] = {
            "locale": self._locale,
            "id": self._mailId
        }
        return self._session.get(MAIL, params=params).json()
