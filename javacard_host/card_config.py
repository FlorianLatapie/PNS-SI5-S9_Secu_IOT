APPLET_AID_PREFIX = [0xa0, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46]  # APPLET AID PREFIX in Common.properties L 24

APPLET_AID = APPLET_AID_PREFIX + [0x10, 0x01]  # l 13 in build.xml
PACKAGE_AID = APPLET_AID_PREFIX + [0x10]  # l 14 in build.xml

APPLET_CLA = 0xB0  # l 43 in java code
PIN_LENGTH = 4  # l 75 in java code

INS_LOGIN = 0x01
INS_MODIFY_PIN = 0x02
INS_DEBUG = 0x03
INS_SIGN_MESSAGE = 0x04
INS_SEND_PUBLIC_KEY = 0x05
INS_FACTORY_RESET = 0x06
INS_GET_RESPONSE = 0xc0  #https://docs.hidglobal.com/crescendo/api/low-level/get-response.htm


# https://www.eftlab.com/knowledge-base/complete-list-of-apdu-responses
SW1_RETRY_WITH_LE = 0x6c
SW1_RETRY_WITH_GET_RESPONSE_61 = 0x61
SW1_RETRY_WITH_GET_RESPONSE_9F = 0x9f



def get_instruction_name(ins: hex):
    results = [key for key, val in globals().items() if val == ins and key.startswith("INS_")]
    if results:
        return results[0][4:]
    return f"{ins:02X}"
