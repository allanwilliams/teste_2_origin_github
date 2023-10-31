
##pip install cryptography
from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings
from urllib.parse import unquote
#this is your "password/ENCRYPT_KEY". keep it in settings.py file
#key = Fernet.generate_key()

def encrypt(txt):
    try:
        # convert integer etc to string first
        txt = str(txt)
        # get the key from settings
        cipher_suite = Fernet(settings.ENCRYPT_KEY) # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('utf-8'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("utf-8")
        return encrypted_text
    except Exception: # pragma: no cover
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(txt):
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("utf-8")
        return unquote(decoded_text)
    except Exception: # pragma: no cover
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None