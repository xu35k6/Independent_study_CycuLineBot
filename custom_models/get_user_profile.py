from linebot import LineBotApi
from linebot.exceptions import LineBotApiError

def getProfile( userid ) :
  #原本的 
  line_bot_api = LineBotApi('') 
  try:
    profile = line_bot_api.get_profile( userid )
      
  except LineBotApiError as e:
    # error handle
    profile = e 

  return profile