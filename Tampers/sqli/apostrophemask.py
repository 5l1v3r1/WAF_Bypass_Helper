from main_modules.settings import PRIORITY, TYPE
__classificationtype__=TYPE.BackEND_SPECIFIED
__priority__ = PRIORITY.HIGH



def tamper(payload, **kwargs):
    """
    Replaces apostrophe character with its UTF-8 full width counterpart

    References:
        * http://www.utf8-chartable.de/unicode-utf8-table.pl?start=65280&number=128
        * http://lukasz.pilorz.net/testy/unicode_conversion/
        * http://sla.ckers.org/forum/read.php?13,11562,11850
        * http://lukasz.pilorz.net/testy/full_width_utf/index.phps

    >>> tamper("1 AND '1'='1")
    '1 AND %EF%BC%871%EF%BC%87=%EF%BC%871'
    """

    return payload.replace('\'', "%EF%BC%87") if payload else payload
