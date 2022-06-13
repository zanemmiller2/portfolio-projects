Author: Zane Miller
Date: 04/13/2022 **updated 4/27/2022
Email: millzane@oregonstate.edu
Description: Instructions and notes for running bloom_filter.py.
Included with submission:
    - README.md
    - Report.txt
    - bloom_filter.py

**Notes:**

- Include bp_dictionary.txt in same directory as bloom_filter.py

**Install py modules:**

- pip install bitarray
- pip install pycryptodomex
     - Note on pycryptodomex: I have had difficulty getting the Crypto.Hash modules to load on my local. 
        * At times I have had to pip uninstall pycrypto, pycryptodome, and pycryptodomex and then re-install pycryptodomex

**Command line execution:**

- python3 bloom_filter.py [bad_password_dictionary] [test_file] [-optional fp]

- [bad_password_dictionary] is the name of the dictionary of bad
  passwords (stored in the same directory as bloom_filter.py)
- test_file is the name of the text file of passwords to test against
  the bloom filter (stored in the same directory as bloom_filter.py)
- optional fp parameter should be passed as a percentage in decimal form - for example if you want to run with a 2% false positivity rate the fp parameter should be .02  
    * The defaulted false positivity rate is 1% if no fp is passed. 
