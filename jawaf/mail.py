from jawaf.server import get_jawaf
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _address_string(addr):
    """Convenience method to treat a given address field as a string or tuple/list
    :param addr: String or List/Tuple. Single address or addresses."""
    if isinstance(addr, str):
        return addr
    return ','.join(addr)


async def send_mail(
    subject, message, from_address, to, cc=None, bcc=None, html_message=None
):
    """Send mail using async smtp lib.
    :param subject: String. Subject.
    :param message: String. Message.
    :param from_address: String. From address.
    :param to: String or List/Tuple. To address.
    :param cc: String or List/Tuple. Email CC.
    :param bcc: String or List/Tuple. Email BCC.
    :param html_message: String. HTML Message (will send multipart message).
    """
    if html_message:
        msg = MIMEMultipart('alternative')
        msg.attach(MIMEText(message, 'plain'))
        msg.attach(MIMEText(html_message, 'html'))
    else:
        msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = _address_string(to)
    if cc:
        msg['Cc'] = _address_string(cc)
    recipients = []
    for address in [to, cc, bcc]:
        if isinstance(address, str):
            address = [address]
        if address:
            recipients.extend(address)
    await get_jawaf().get_smtp().sendmail(from_address, recipients, msg.as_string())
