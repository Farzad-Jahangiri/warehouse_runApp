from typing import TypedDict, Optional
from datetime import datetime

class UserData(TypedDict):
    id: int
    step: str
    number: int
    number_user: int
    last_settlement_at: datetime
    lang: str
    warranty: int
    chat_id: int
    password: Optional[str]
    api_id: Optional[str]
    state: str
    code: Optional[str]
    message: Optional[str]
    api_hash: Optional[str]
    deviceModel: Optional[str]
    systemVersion: Optional[str]
    createdAt: datetime
    updatedAt: datetime
    phone: str
    isRunApp: bool
    pId: str
    is_closed: bool
    callbackquery_id: str
    message_id:str
    appVersionStr: str
    appVersion: int
    captcha: bool


