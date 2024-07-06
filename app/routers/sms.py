from fastapi import APIRouter, Depends, HTTPException, status
from app.middleware.auth import auth_required, get_current_user
from app.utils import authenticate_user,create_access_token
from app import settings
import logging
from pydantic import BaseModel
import requests
import json
from typing import List
logger = logging.getLogger(__name__)
router = APIRouter()
    
class SmsRequest(BaseModel):
    campaign_name: str
    originator: str
    recipients: List[str] 
    content: str
    
    
@router.post("/sms")
@auth_required
async def sms_sender(sms_data:SmsRequest, current_user: str = Depends(get_current_user)):
    campaign_name = sms_data.campaign_name
    originator = sms_data.originator
    recipients = sms_data.recipients  
    content = sms_data.content  
    url = settings.URL

    payload = json.dumps({
    "messages": [
        {
        "channel": "sms",
        "recipients": recipients,
        "content": content,
        "msg_type": "text",
        "data_coding": "text"
        }
    ],
    "message_globals": {
        "originator": originator,
        "report_url": "https://the_url_to_recieve_delivery_report.com"
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer '+settings.API_TOKEN
    }

    #TODO Handle error cases (due to lack of time i did'nt handle the error cases)
    
    response = requests.request("POST", url, headers=headers, data=payload)
    logger.info("sms info: %s", response)
    data=response.text
    return data