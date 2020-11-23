import itertools
import os
import subprocess
from email.parser import Parser
from email.header import decode_header

SYNC_CMD = ('mbsync', '-a')
MAILBOX_DIR = '.local/share/mail'
NEW_MAIL_DIR = 'INBOX/new'

class Message():

    parser = Parser()
    headers = ('To', 'From', 'Subject', 'Date')

    def __init__(self, path):
        with open(path, 'r') as f:
            m = PARSER.parse(f)
        for h in self.headers:
            hdr = ''.join((self.decode(chunk) for chunk in decode_header(m[h])))
            setattr(self, h, hdr)

    @staticmethod
    def decode(chunk):
        (bytes, encoding) = chunk
        return (bytes if isinstance(bytes, str) else bytes.decode()) \
                if encoding is None else bytes.decode(encoding)

    def __lt__(self, other):
        return self.To < other.To


class Report():

    def __init__(self, messages):
        self.messages = list(messages)
        self.count = len(self.messages)
        self.messages.sort()

    def notify(self):
        subprocess.run(('notify-send', '--icon=mail-unread', self.title(), self.html()))

    def title(self):
        return 'You have {} new message(s)!'.format(self.count)

    def html(self):
        (trimmed, messages) = (True, itertools.take(5, self.messages)) \
            if self.count > 5 else (False, self.messages)
        return '<br/><br/>'.join(self.item(m) for m in messages) \
                + ('<li>...</li>' if trimmed else '')

    @staticmethod
    def item(msg):
        return 'From: {}<br/>To: {}<br/>Subject: {}<br/>Date: {}'.format(
                msg.From,
                msg.To,
                msg.Subject,
                msg.Date
            )


def scan(mailboxes):
    for dir in mailboxes:
        for file in os.listdir(dir):
            yield os.path.join(dir, file)


def main():
    mailboxes_dir = os.path.join(os.getenv('HOME'), MAILBOX_DIR)
    mailbox_names = os.listdir(mailboxes_dir)
    mailboxes = [os.path.join(mailboxes_dir, m, NEW_MAIL_DIR) for m in mailbox_names]

    old = set(scan(mailboxes))
    subprocess.run(('mbsync', '-a'))
    new = set(scan(mailboxes)) - old
    r = Report((Message(f) for f in new))
    if r.count > 0:
        r.notify()


if __name__ == '__main__':
    main()
