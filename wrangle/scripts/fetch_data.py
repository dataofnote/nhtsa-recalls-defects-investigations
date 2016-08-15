from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse, urlunparse
from zipfile import ZipFile

import requests
FETCHED_DIR = Path('wrangle', 'corral', 'fetched')
DEST_DATA_DIR = FETCHED_DIR / 'data'
DEST_DATA_DIR.mkdir(exist_ok=True, parents=True)

DEST_HEADERS_DIR = FETCHED_DIR / 'headers'
DEST_HEADERS_DIR.mkdir(exist_ok=True, parents=True)

SRC_URLS = [
    'http://www-odi.nhtsa.dot.gov/downloads/folders/Complaints/FLAT_CMPL.zip',
    'http://www-odi.nhtsa.dot.gov/downloads/folders/Investigations/FLAT_INV.zip',
    'http://www-odi.nhtsa.dot.gov/downloads/folders/Recalls/FLAT_RCL.zip',
    'http://www-odi.nhtsa.dot.gov/downloads/folders/Recalls/FLAT_RCL_Qtrly_Rpts.zip',
    'http://www-odi.nhtsa.dot.gov/downloads/folders/TSBS/FLAT_TSBS.zip'
]

def main():
    for url in SRC_URLS:
        # Download headers
        headerurl = url.replace('FLAT_', '').replace('.zip', '.txt')
        print("Downloading:", headerurl)
        hresp = requests.get(headerurl)
        # save it as an all-lower case filename
        header_destname = DEST_HEADERS_DIR / Path(headerurl).name.lower()
        print("Saving to:", header_destname)
        header_destname.write_text(hresp.text)

        # Download the data zip file
        print("Downloading:", url)
        resp = requests.get(url)
        print("Unzipping into:", DEST_DATA_DIR)
        with ZipFile(BytesIO(resp.content)) as zfile:
            for f in zfile.filelist:
                # save it as an all-lower case filename
                destname = DEST_DATA_DIR / f.filename.lower()
                print("\tUnzipping:", f.filename, "as:", destname)
                destname.write_bytes(zfile.read(f.filename))




if __name__ == '__main__':
    main()
