from pathlib import Path
from sys import argv
import re

HEADERS_DIR = Path('wrangle', 'corral', 'fetched', 'headers')
FIELD_PATTERN = re.compile(r'^(\d+) +([A-Z_0-9]+) + ([A-Z]+)\((\d+)\)')

######
#The file looks like this:

# Last updated: September 29, 2015

# FIELDS:
# =======

# Field#  Name              Type/Size     Description
# ------  ---------         ---------     --------------------------------------
# 1       CMPLID            CHAR(9)       NHTSA'S INTERNAL UNIQUE SEQUENCE NUMBER.
#                                         IS AN UPDATEABLE FIELD,THUS DATA FOR A
#                                         GIVEN RECORD POTENTIALLY COULD CHANGE FROM
#                                         ONE DATA OUTPUT FILE TO THE NEXT.
# 2       ODINO             CHAR(9)       NHTSA'S INTERNAL REFERENCE NUMBER.
#                                         THIS NUMBER MAY BE REPEATED FOR
#                                         MULTIPLE COMPONENTS.

def extract_headers_from_file(filestub):
    """
    filestub: String; e.g. "cmpl"

    Returns: List; a list of strings corresponding to headers
    """
    filename = filestub + '.txt'
    headers = []
    start_parsing = False
    srcname = HEADERS_DIR / filename
    for line in srcname.open('r'):
        if not start_parsing:
            if 'Field#' in line:
                start_parsing = True
            else:
                pass

        else:
            fmatch = FIELD_PATTERN.match(line)
            if fmatch:
                headers.append(fmatch.groups()[1])
    return headers


if __name__ == '__main__':
    print(",".join(extract_headers_from_file(argv[1])))




