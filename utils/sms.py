from kavenegar import *


def send_code(code,phone=None):
    api = KavenegarAPI('4D333164373941442B567851646D7644467161545665635551685A624379465A484E6A724473496D4F59343D')
    params = {'sender': '2000660110',
              'receptor': '09157890381',
              'message': code
              }
    api.sms_send(params=params)

def send_message(message,phone=None):
    api = KavenegarAPI('4D333164373941442B567851646D7644467161545665635551685A624379465A484E6A724473496D4F59343D')
    params = {
        'sender': '2000660110',
        'receptor': '09157890381',
        'message': message
    }
    api.sms_send(params=params)





