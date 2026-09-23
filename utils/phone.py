import re
import phonenumbers
from phonenumbers import geocoder, carrier, NumberParseException
from typing import Tuple, Optional
from phonenumbers import region_code_for_country_code

def extract_telegram_code(text: str) -> str | None:
    """
    Extracts Telegram login code (usually 4-6 digits) from a given text.
    
    Args:
        text (str): The text containing the Telegram code.
    
    Returns:
        str | None: The extracted code if found, otherwise None.
    """
    # Regular expression to match 4-6 digit codes
    match = re.search(r'\b(\d{4,6})\b', text)
    if match:
        return match.group(1)
    return None

def parse_phone_input(text: str):
    """
    Expected format:
    +1 6843360588
    """
    try:
        pattern = r"^\+(\d{1,4})\s*(\d{6,15})$"
        match = re.match(pattern, text)
        
        if not match:
            return None, (
            "❌ فرمت شماره نامعتبر است.\n\n"
            "لطفاً شماره تلفن خود را به این شکل ارسال کنید:\n"
            "+1 6843360588\n\n"
            "مثال:\n"
            "+44 7911123456"
        )

        num = phonenumbers.parse(text, None)
        country_code = str(num.country_code)
        phone_number =  text[1 + len(country_code):]

        return {
            "country_code": country_code,
            "phone_number": phone_number,
            "full_number": f"{country_code}{phone_number}"
        }, None
    except Exception as e:
        print("Error: ", e)
        return None, (
            "❌ فرمت شماره نامعتبر است.\n\n"
            "لطفاً شماره تلفن خود را به این شکل ارسال کنید:\n"
            "+1 6843360588\n\n"
            "مثال:\n"
            "+44 7911123456"
        )




COUNTRY_CALLING_CODES = sorted([
    "1","7",
    "20","27","30","31","32","33","34","36","39","40","41","43","44","45",
    "46","47","48","49",
    "51","52","53","54","55","56","57","58",
    "60","61","62","63","64","65","66",
    "81","82","84","86",
    "90","91","92","93","94","95","98",
    "211","212","213","216","218",
    "220","221","222","223","224","225","226","227","228","229",
    "230","231","232","233","234","235","236","237","238","239",
    "240","241","242","243","244","245","246","247","248","249",
    "250","251","252","253","254","255","256","257","258","260",
    "261","262","263","264","265","266","267","268","269",
    "290","291",
    "350","351","352","353","354","355","356","357","358","359",
    "370","371","372","373","374","375","376","377","378","379",
    "380","381","382","383","385","386","387","389",
    "420","421","423",
    "500","501","502","503","504","505","506","507","508","509",
    "590","591","592","593","594","595","596","597","598","599",
    "670","672","673","674","675","676","677","678","679",
    "680","681","682","683","685","686","687","688","689",
    "690","691","692",
    "800","808","870","871","872","873","874","878",
    "881","882","883","888","979"
], key=len, reverse=True)  # مهم: اول کدهای بلندتر

# def split_phone_number(phone: str) -> tuple[str, str]:
    
#     if not phone.startswith("+"):
#         raise ValueError("Phone number must start with '+'")
#     num = phonenumbers.parse(phone, None)
#     country_code = num.country_code
#     phone_number =  num.national_number
#     print("country_code:",country_code)
#     print("phone_number:",phone_number)

   

#     return country_code, phone_number
def split_phone_number(phone: str) -> tuple[str, str]:
    if not phone.startswith("+"):
        raise ValueError("Phone number must start with '+'")

    num = phonenumbers.parse(phone, None)

    country_code = str(num.country_code)
    
    real_number = phone[1 + len(country_code):]

    return country_code, real_number


def parse_country_price(text: str) -> Optional[Tuple[str, float]]:
    """
    این تابع متن ادمین را گرفته و:
    - کد کشور را بدون + برمی‌گرداند
    - قیمت را به صورت عدد برمی‌گرداند
    
    متن باید در دو خط باشد:
    خط اول: کد کشور با + (مثلاً +98)
    خط دوم: قیمت (مثلاً 15000)
    
    اگر متن معتبر نباشد، None برمی‌گرداند.
    """

    try:
        # VALID_COUNTRY_CODES = sorted([str(code) for code in phonenumbers.supported_calling_codes()], key=int)

        # print("VALID_COUNTRY_CODES: ", VALID_COUNTRY_CODES, len(VALID_COUNTRY_CODES))
        lines = text.strip().splitlines()
        if len(lines) < 2:
            return None

        country_code_line = lines[0].strip()
        price_line = lines[1].strip()
        # پاک کردن + از کد کشور
        country_code_line = country_code_line.replace("+", "").strip()

        # بررسی معتبر بودن کد کشور با phonenumbers
        region = region_code_for_country_code(int(country_code_line))

        if region == "ZZ":
            print(f"خطا: کد کشور {country_code_line} در دیتابیس جهانی یافت نشد.")
            return None
        
        # استخراج عدد از قیمت
        price_numbers = re.findall(r"\d+(?:\.\d+)?", price_line.replace(",", ""))
        if not price_numbers:
            return None
        price = float(price_numbers[0])

        return country_code_line, price

    except Exception:
        return None