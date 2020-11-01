import math
import subprocess
import random
import string
from .models import *


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def is_authenticated(request):
    if 'userid' in request.session:
        return True
    return False


def generateRandomPassword():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(random.choice(alphabet) for i in range(8))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password


def dictStringToReadableString(dictString, field=None):
    if field == 'info':
        dictString = str(dictString).replace('[', '')
        dictString = str(dictString).replace(']', '')
        dictString = dictString.replace(',', '\n')
    dictString = str(dictString).replace('\'', '')
    return dictString


def filterCpuString(cpuString):
    cpuString = cpuString.replace('(R)', '')
    cpuString = cpuString.replace('CPU ', '')
    cpuString = cpuString.replace('(TM) Processor', '')
    cpuString = cpuString.replace('(tm) Processor', '')
    return cpuString
