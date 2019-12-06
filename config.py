import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dfak-9rehgha-93[atistujdagcm/09ga'
    