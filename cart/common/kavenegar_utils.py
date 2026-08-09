# kavenegar_utils.py
from kavenegar import KavenegarAPI, APIException, HTTPException
from django.conf import settings


def send_sms(receptor: str, message: str) -> bool:
    try:
        # settings.KAVENEGAR_API_KEY
        api = KavenegarAPI('382B63416131706353324446375962696F4D377A3548786D533653516C4456346948744B6A737972414D383D')
        api.sms_send({
            'sender': '2000660110',
            'receptor': receptor,
            'message': message,
        })
        return True
    except (APIException, HTTPException) as e:
        print(f"[Kavenegar] send_sms error: {e}")
        return False


# def send_lookup(receptor: str, template: str, token: str) -> bool:
#     try:
#         api = KavenegarAPI('382B63416131706353324446375962696F4D377A3548786D533653516C4456346948744B6A737972414D383D')
#         api.verify_lookup({
#             'receptor': receptor,
#             'template': template,
#             'token': token,
#         })
#         return True
#     except (APIException, HTTPException) as e:
#         print(f"[Kavenegar] send_lookup error: {e}")
#         return False





# template => در بخش اعتبارسنجی سایت کاوخ نگار مشخص کردیم . 
def send_lookup(receptor: str, template: str, tokens: dict) -> bool:
    try:
        api = KavenegarAPI('382B63416131706353324446375962696F4D377A3548786D533653516C4456346948744B6A737972414D383D')
        params = {
            'receptor': receptor,
            'template': template,
            'token':  tokens.get('token', ''),
            'token2': tokens.get('token2', ''),
            'token3': tokens.get('token3', ''),
        }
        api.verify_lookup(params)
        return True
    except (APIException, HTTPException) as e:
        print(f"[Kavenegar] send_lookup error: {e}")
        return False

