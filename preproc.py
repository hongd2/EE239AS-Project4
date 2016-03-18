
# coding: utf-8

# In[ ]:

from os import listdir
from feature_extract import feature_extract

files = listdir('../tweet_data')
print(files)

from os.path import splitext

import re

for fname in files:
    m = re.search('#.+', splitext(files[0])[0])
    if m:
        hashtag = m.group()
        print("Processing '%s'" % hashtag)
    outfile = splitext(fname)[0] + '.csv'
    print("Output file name '%s'" % outfile)

    f_handle = open('../tweet_data/'+fname, encoding="utf8")
    feature_extract(f_handle, outfile)
    f_handle.close()
    #import pdb; pdb.set_trace()

