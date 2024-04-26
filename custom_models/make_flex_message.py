import copy
from custom_models import Bubble

def make_course_search_flex(a_list) : # a_list = [(課程名稱, 授課老師, 上課時間, 上課地點), (...), (...)]
    
    #從Bubble.py導入字典Bubble_Type
    
    A_bubble_1 = Bubble.Bubble_Type_1
    A_bubble_2 = Bubble.Bubble_Type_2
    A_bubble_3 = Bubble.Bubble_Type_3
    # print(type(A_bubble)) #dict
    #創造一個contents
    contents = { "type": "carousel","contents": [] }
    # print(contents)
    while len(a_list) != 0 :
        i = 0 
        a_course_data = a_list[0] # 課程資訊(all)
        course_name = a_course_data[i]  # 課程名稱
        i = i + 1
        course_type = a_course_data[i]  # 課程類別
        i = i + 1
        teacher = a_course_data[i] # 授課老師  
        i = i + 1
        time = a_course_data[i] # 上課時間
        i = i + 1
        place = a_course_data[i] # 上課地點
        time_place_1 = time + '  ' + place 
        i = i + 1
        # 判斷有沒有下一個時間段
        ch = str( a_course_data[i] )
        ch = ch[0]
        if ( ch == '1' or ch == '2' or ch == '3' or ch == '4' or ch == '5' or ch == '6' or ch == '7' ) :
            time = a_course_data[i]
            i = i + 1
            place = a_course_data[i]
            time_place_2 = time + '  ' + place 
            i = i + 1 
            # 判斷有沒有下一個時間段
            ch = str( a_course_data[i] )
            ch = ch[0]
            if ( ch == '1' or ch == '2' or ch == '3' or ch == '4' or ch == '5' or ch == '6' or ch == '7' ) : # 有三個課程時間
                time = a_course_data[i]
                i = i + 1
                place = a_course_data[i]
                time_place_3 = time + '  ' + place 
                i = i + 1 
                course_id = a_course_data[i]
                course_id = course_id
                A_NEW_bubble = copy.deepcopy(A_bubble_3)               
                A_NEW_bubble["body"]["contents"][0]["text"] = course_name # 課程名稱   
                A_NEW_bubble["body"]["contents"][1]["text"] = course_type # 課程類別                
                A_NEW_bubble["body"]["contents"][2]["text"] = teacher # 授課老師           
                A_NEW_bubble["body"]["contents"][3]["text"] = time_place_1 # 上課時間1   
                A_NEW_bubble["body"]["contents"][4]["text"] = time_place_2 # 上課時間2
                A_NEW_bubble["body"]["contents"][5]["text"] = time_place_3 # 上課時間3                 
                A_NEW_bubble["footer"]["contents"][0]["action"]["text"] = course_id # 加入我的課表編號
                contents["contents"].append(A_NEW_bubble)
            else : # 有兩個課程時間
                course_id = a_course_data[i]
                course_id = course_id
                A_NEW_bubble = copy.deepcopy(A_bubble_2)               
                A_NEW_bubble["body"]["contents"][0]["text"] = course_name # 課程名稱   
                A_NEW_bubble["body"]["contents"][1]["text"] = course_type # 課程類別                
                A_NEW_bubble["body"]["contents"][2]["text"] = teacher # 授課老師           
                A_NEW_bubble["body"]["contents"][3]["text"] = time_place_1 # 上課時間1   
                A_NEW_bubble["body"]["contents"][4]["text"] = time_place_2 # 上課時間2              
                A_NEW_bubble["footer"]["contents"][0]["action"]["text"] = course_id # 加入我的課表編號
                contents["contents"].append(A_NEW_bubble)
                
        else : # 只有一個時間段的課
            course_id = a_course_data[i]
            course_id = course_id
            A_NEW_bubble = copy.deepcopy(A_bubble_1)               
            A_NEW_bubble["body"]["contents"][0]["text"] = course_name # 課程名稱   
            A_NEW_bubble["body"]["contents"][1]["text"] = course_type # 課程類別                
            A_NEW_bubble["body"]["contents"][2]["text"] = teacher # 授課老師           
            A_NEW_bubble["body"]["contents"][3]["text"] = time_place_1 # 上課時間1                    
            A_NEW_bubble["footer"]["contents"][0]["action"]["text"] = course_id # 加入我的課表編號
            contents["contents"].append(A_NEW_bubble)

        a_list.pop(0)  

    # print(contents)
    return contents