# -*- coding: utf-8 -*-

import json, os


README_URL = os.environ['INC_TEST__README_URL']

MAIN_INCLUDED_URL = os.environ['INC_TEST__MAIN_INCLUDED_URL']

FETCH_DIR_URL= os.environ['INC_TEST__FETCH_URL_ROOT_DIR']
if FETCH_DIR_URL[-1:] is not '/':  # since the server may or may not result in the '/', let's make the setting predictable
    FETCH_DIR_URL = '%s/' % FETCH_DIR_URL


