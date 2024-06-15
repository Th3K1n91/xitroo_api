from datetime import datetime
from .Inbox import Inbox as Inboxclass
class SearchMail:
    # {'totalMails': 0, 'mails': []}
    def __init__(self, xitroo):
        """
        SearchMail constructor.
        :param xitroo: Xitroo object.
        :type xitroo: :class:`xitroo.Xitroo.Xitroo`
        """
        self._xitroo = xitroo
        self._mails: dict = self._xitroo.getRawInbox()
        self._result: dict = {'totalMails': 0, 'mails': []}

    def byDate(self, mailDate: str) -> Inboxclass:
        """
        SearchMail by date.
        :param mailDate: mail date as %Y-%m-%d.
        :type mailDate: :class:`str`
        :return: :class:`Inboxclass`
        """
        # datetime.strptime(mailDate, "%Y-%m-%d").date()
        for i in self._mails['mails']:
            id: str = i['_id']
            if datetime.fromtimestamp(i['arrivalTimestamp']).strftime('%Y-%m-%d') == mailDate:
                for j in self._result['mails']:
                    if id in j['_id']:
                        return self._xitroo.Inbox(inbox=self._result)
                self._result['totalMails'] += 1
                self._result['mails'].append(i)
        return self._xitroo.Inbox(inbox=self._result)

    def bySender(self, sender: str) -> Inboxclass:
        """
        SearchMail in sender.
        :param sender: sender as string.
        :type sender: :class:`str`
        :return: :class:`Inboxclass`
        """
        for i in self._mails['mails']:
            id: str = i['_id']
            if sender in self._xitroo.Mail(id).getFromMail():
                for j in self._result['mails']:
                    if id in j['_id']:
                        return self._xitroo.Inbox(inbox=self._result)
                self._result['totalMails'] += 1
                self._result['mails'].append(i)
        return self._xitroo.Inbox(inbox=self._result)

    def byTitle(self, title: str) -> Inboxclass:
        """
        SearchMail in title.
        :param title: title as string.
        :type title: :class:`str`
        :return: :class:`Inboxclass`
        """
        for i in self._mails['mails']:
            id: str = i['_id']
            if title in self._xitroo.Mail(id).getSubject():
                for j in self._result['mails']:
                    if id in j['_id']:
                        return self._xitroo.Inbox(inbox=self._result)
                self._result['totalMails'] += 1
                self._result['mails'].append(i)
        return self._xitroo.Inbox(inbox=self._result)

    def byTextInBody(self, text: str) -> Inboxclass:
        """
        SearchMail in text body.
        :param text: text as string.
        :type text: :class:`str`
        :return: :class:`Inboxclass`
        """
        for i in self._mails['mails']:
            id: str = i['_id']
            if text in self._xitroo.Mail(id).getBodyText():
                for j in self._result['mails']:
                    if id in j['_id']:
                        return self._xitroo.Inbox(inbox=self._result)
                self._result['totalMails'] += 1
                self._result['mails'].append(i)
        return self._xitroo.Inbox(inbox=self._result)

    # def searchInboxRegex(self):
    #     # {'totalMails': 0, 'mails': []}
    #     class SearchRe:
    #         def __init__(self, xitroo: Xitroo):
    #
    #         def byDate(self, regex: str):
    #                 if re.search(regex, datetime.fromtimestamp(i['arrivalTimestamp']).strftime('%Y-%m-%d')):
    #
    #         def bySender(self, regex: str):
    #                 if re.search(regex, self._xitroo.Mail(id).getFromMail()):
    #
    #         def byTitle(self, regex: str):
    #                 if re.search(regex, self._xitroo.Mail(id).getSubject()):
    #
    #         def byTextInBody(self, regex: str):
    #                 if re.search(regex, self._xitroo.Mail(id).getBodyText()):
    #     return SearchRe(self)
