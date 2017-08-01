#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

from main_modules.settings import PRIORITY, TYPE
__classificationtype__=TYPE.BackEND_SPECIFIED

__priority__ = PRIORITY.HIGHEST

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Replaces instances like 'IFNULL(A, B)' with 'IF(ISNULL(A), B, A)'

    Requirement:
        * MySQL
        * SQLite (possibly)
        * SAP MaxDB (possibly)

    Tested against:
        * MySQL 5.0 and 5.5

    Notes:
        * Useful to bypass very weak and bespoke web application firewalls
          that filter the IFNULL() function

    >>> tamper('IFNULL(1, 2)')
    'IF(ISNULL(1),2,1)'
    """

    if payload and payload.find("IFNULL") > -1:
        while payload.find("IFNULL(") > -1:
            index = payload.find("IFNULL(")
            depth = 1
            comma, end = None, None

            for i in xrange(index + len("IFNULL("), len(payload)):
                if depth == 1 and payload[i] == ',':
                    comma = i

                elif depth == 1 and payload[i] == ')':
                    end = i
                    break

                elif payload[i] == '(':
                    depth += 1

                elif payload[i] == ')':
                    depth -= 1

            if comma and end:
                _ = payload[index + len("IFNULL("):comma]
                __ = payload[comma + 1:end].lstrip()
                newVal = "IF(ISNULL(%s),%s,%s)" % (_, __, _)
                payload = payload[:index] + newVal + payload[end + 1:]
            else:
                break

    return payload
