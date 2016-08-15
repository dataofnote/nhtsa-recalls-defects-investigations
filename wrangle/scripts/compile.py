"""
Attaches fetched data file to headers, saves as CSV in wrangle/corral/compiled
"""

from csv import DictWriter, DictReader
from pathlib import Path
from parse_headers import extract_headers_from_file
from sys import argv

import requests
FETCHED_DIR = Path('wrangle', 'corral', 'fetched')
COMPILED_DIR = Path('wrangle', 'corral', 'compiled')
COMPILED_DIR.mkdir(exist_ok=True, parents=True)

DATANAME_MAP = {
    'complaints': 'cmpl',
    'investigations': 'inv',
    'recalls': 'rcl',
    'recalls_quarterly_reports': 'rcl_qtrly_rpts',
    'technical_service_bulletins': 'tsbs',
}



def compile(readable_name):
    raw_name = DATANAME_MAP[readable_name]
    src_path = FETCHED_DIR / 'data' / 'flat_{}.txt'.format(raw_name)
    dest_path =  COMPILED_DIR / (readable_name + '.csv')

    headers = extract_headers_from_file(raw_name)
    print("Headers:", ', '.join(headers))


    destfile = dest_path.open('w')
    destcsv = DictWriter(destfile, fieldnames = headers)
    destcsv.writeheader()

    print("Opening:", src_path)
    print("Writing to:", dest_path)
    with src_path.open('r', encoding='latin-1') as srcfile:
        srccsv = DictReader(srcfile, delimiter='\t', fieldnames=headers)
        for i, row in enumerate(srccsv):
            try:
                destcsv.writerow(row)
            except Exception as err:
                print("\n\n", err)
                print("%s: %s" % (i, row))


    destfile.close()



if __name__ == '__main__':
    compile(argv[1])

