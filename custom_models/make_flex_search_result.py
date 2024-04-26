import copy
#copy.deepcopy(a)
from custom_models import get_user_profile, Bubble
def set_flex_search_result( result, userid ) :
  userName = get_user_profile.getProfile(userid).display_name 
  #從Bubble.py導入字典Bubble_Type
  
  A_bubble = Bubble.Bubble_Type
  print(type(A_bubble)) #dict

    #創造一個contents
  contents = { "type": "carousel","contents": [] }
  print(contents)

  A_NEW_bubble = copy.deepcopy(A_bubble)
  string = result[0]
        #bubble裡面的地一個Box的標題
  A_NEW_bubble["body"]["contents"][0]["text"] = '嗨！ ' + userName + '\n' + '你可能會想看這個：' + '\n\n' + string
        
  string = result[1]
        #bubble裡面的地一個Box的標提裡面暗藏的網址
  A_NEW_bubble["body"]["contents"][0]["action"]["uri"] = string
        
  string = result[2]     
        #bubble裡面的地一個Box的照片網址
  A_NEW_bubble["header"]["contents"][0]["url"] = string
            
  contents["contents"].append(A_NEW_bubble)

  print(contents)
  return contents
