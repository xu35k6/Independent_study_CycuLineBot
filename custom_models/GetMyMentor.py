import requests
from lxml import html
from bs4 import BeautifulSoup
#from selenium import webdriver
from custom_models import ClassLearned

def GetMyMentor( id, UserID, UserPasswd, db ) :
    LOGIN_URL = 'https://cmap.cycu.edu.tw:8443/MyMentor/stdLogin.do'# 登入MyMentor
    COURSE_HETORY_URL = 'https://cmap.cycu.edu.tw:8443/MyMentor/courseCreditStructure.do' # 畢業門檻-修課紀錄

    session_requests = requests.session()

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36'
        # 'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
    }

    login_data = {'userId': UserID, 'password': UserPasswd }

    my_mentor = session_requests.post(LOGIN_URL, data = login_data, headers = headers ) # 登入MyMentor 


    r = session_requests.get(COURSE_HETORY_URL, allow_redirects = False, headers = headers ) # 取得畢業門檻-修課紀錄
    soup = BeautifulSoup(r.text, 'lxml')
    soup.encoding = 'utf-8'

    if ( r.text.find(UserID) == -1 ) :
        print('失敗')
        return None
    else :
        print( "登入成功" )
        query = { "UserID" : id }
        # 目前只做到106~109年進來的學生
        semester_list = ['1061', '1062', '1071', '1072', '1081', '1082', '1091', '1092', '1101', '1102', '1111', '1112', '1121', '1122']
        AtoZ_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z' ]
        paragraphs = soup.find_all('td') # 所有修課紀錄
        content = []  # 放所有修課紀錄(包含尚未修的課程)
        count = 0
        for p in paragraphs: # 將所有修課紀錄都放到content中       
            stem = p.text
            stem = stem.strip()
            content.append( stem )

        # 分類 尚未/已修 課程
        must_list = [] # 尚未修過的必修課
        course_list = [] # 已修課程表
        fail_list = [] # 被當的課
        civics_list = [] # 公民課list
        history_list = [] # 歷史課list 
        wu_list = [] # 基礎物類list
        wo_list = [] # 基礎我類list
        hasCivics = False # 是否修過公民課(被當則為False)
        hasHistory = False # 是否修過歷史課
        hasWu_basic = False  # 是否修過基礎物類
        hasWo_basic = True  # 是否修過基礎我類 ( 兩門都必須要修 所以init為 True)
        # 實在是不知道 天 人 物 我 要用什麼英文 於是使用羅馬拼音
        # 天 tain
        # 人 ren
        # 物 wu
        # 我 wo
        elective_course_list = [] # 已修過的延伸通識選修(延伸天人物我)
        elective_counter = 0 # 計算已修過多少延伸通識選修
        hasTain = False # 是否修過天_延伸
        hasRen = False # 是否修過人_延伸
        hasWu = False # 是否修過物_延伸
        hasWo = False # 是否修過我_延伸
        i = 0
        # for a in range(len(content)):
        #     print(a,content[a])
        while ( i < len(content) ) : 
            stem = str( content[i] )
            if ( stem == '' ) : # 空的就往下讀
                i = i + 1 
            elif  ( stem == "基本知能" ) :
                PE_counter = 0 # 算已修過多少門體育
                i = i + 1 
                print( "--------------------START------------------------")

                while ( str(content[i]) != "基本知能 體育興趣至少需修4個" ) : # 把基本知能裡面課程的都讀完
                    stem = str( content[i] )
                    category = '基本知能'
                    if ( stem == '' ) :
                        None
                    elif ( stem[0] in AtoZ_list ) : # 前面先有三個item 才是修過的課
                        course_code = str( content[i] ) # 課程代碼
                        i = i + 1 
                        course_name = str( content[i] ) # 課程名稱
                        i = i + 1 
                        credit = str( content[i] ) # 學分數
                        i = i + 1 
                        while(str( content[i] ) == ''):
                            i = i + 1
                        stem = str( content[i] ) # 有修過就會是 1092之類的 沒修過應該是0 或是 ''
                        
                        if stem not in semester_list : # 尚未修此課程
                            must_list.append( [course_code, category, course_name, credit] ) # ZA199 體育 0
                            i = i + 1
                        else : # 修過此課程
                            semester = str( content[i] ) # 學期
                            i = i + 1
                            course_code = str( content[i] ) # 課程代碼
                            i = i + 1
                            course_name = str( content[i] ) # 課程名稱
                            i = i + 3
                            credit = str( content[i] ) # 學分數
                            i = i + 1 
                            if ( str(content[i]) != '' ) : # 成績及格(有成績) (被當的沒成績)
                                score = str( content[i] )
                                course_list.append( [semester, course_code, course_name, credit, score] ) # 1072 ZA612 英語聽講(二) 1 92 
                            else : # 被當
                                fail_list.append( [course_code, course_name, credit] )
                    else : # 修過的課 (如 體育課) 
                        semester = str( content[i] ) # 學期
                        i = i + 1
                        course_code = str( content[i] ) # 課程代碼
                        if ( course_code[0:2] == "GR" ) : # 是體育課
                            PE_counter = PE_counter + 1
                        i = i + 1
                        course_name = str( content[i] ) # 課程名稱
                        i = i + 3
                        credit = str( content[i] ) # 學分數
                        i = i + 1 
                        if ( str(content[i]) != '' ) : # 成績及格(有成績) (被當的沒成績)
                            score = str( content[i] )
                            course_list.append( [semester, course_code, course_name, credit, score] ) # 1072 ZA612 英語聽講(二) 1 92 
                        else : # 被當
                            fail_list.append( [course_code, course_name, credit] )               
                    i = i + 1 # 換下一筆資料
                    
                # end while 把基本知能裡面的都讀完
                i = i + 3 # 第3格以後才是學分

                total_credit = content[i] # 基本知能的總學分 
                query['基本知能總學分'] = total_credit
                if ( PE_counter < 4 ) :
                    query['體育學分_未修'] = 4 - PE_counter
                else :
                    query['體育學分_未修'] = 0

                query['基本知能_已修'] = course_list
                query['基本知能_未修'] = must_list
                query['基本知能_被當'] = fail_list
                i = i + 1 # 下次迴圈直接是下筆資料
                must_list = [] # 尚未修過的必修課
                course_list = [] # 已修課程表
                fail_list = [] # 被當的課
            # end elif stem == "基本知能"
            elif ( stem == "天類" ) :
                # 分類 尚未/已修 課程
                category = '宗哲'
                i = i + 1
                course_code = str( content[i] ) # 課程代碼
                i = i + 1 
                course_name = str( content[i] ) # 課程名稱
                i = i + 1
                while ( str( content[i] ) == '' ) : # 把空格讀掉
                    i = i + 1
                if ( str( content[i] ) in semester_list ) : # 有修過此堂課( 宗教哲學 )
                    semester = str( content[i] ) 
                    i = i + 1
                    course_code = str( content[i] )
                    i = i + 1
                    course_name = str( content[i] )
                    i = i + 1 # 性質: 半
                    i = i + 1 # 學期 下
                    i = i + 1 
                    credit = str( content[i] )
                    i = i + 1
                    score = str( content[i] )
                    
                    if ( score == '' ) : # 被當
                        fail_list.append( [course_code, category, course_name, credit] )
                    else : # 已修過
                        course_list.append( [semester, course_code, category, course_name, credit, score] ) # 1082 GQ101 宗哲 宗教哲學 2 93
                else : # 沒修過( 宗教哲學 ) 此格會是0 代表0學分
                    must_list.append( [course_code,  category, course_name, credit] ) # GQ101 宗教哲學 
                
                i = i + 2 # 人生哲學的課程代碼 有多一隔空格
                category = '人哲'
                course_code = str( content[i] ) # 課程代碼
                i = i + 1 
                course_name = str( content[i] ) # 課程名稱
                i = i + 1
                while ( str( content[i] ) == '' ) : # 把空格讀掉
                    i = i + 1
                if ( str( content[i] ) in semester_list ) : # 有修過此堂課( 人生哲學 )
                    semester = str( content[i] ) 
                    i = i + 1
                    course_code = str( content[i] )
                    i = i + 1
                    course_name = str( content[i] )
                    i = i + 1 # 性質: 半
                    i = i + 1 # 學期 下
                    i = i + 1 
                    credit = str( content[i] )
                    i = i + 1
                    score = str( content[i] )
                    
                    if ( score == '' ) : # 被當
                        fail_list.append( [course_code, category, course_name, credit] )
                    else : # 已修過
                        course_list.append( [semester, course_code, category, course_name, credit, score] ) # 1082 GQ101 人哲 人生哲學 2 93
                else : # 沒修過( 人生哲學 ) 此格會是0 代表0學分
                    must_list.append( [course_code, category, course_name, credit] ) # GQ101 人生哲學 

                i = i + 1 # 下次迴圈直接是下筆資料
            # end elif stem == "天類"
            elif ( stem == "人類" ) :
                civics_list = [] # 公民課list
                hasCivics = False # 是否修過公民課(被當則為False)
                # 將所有公民課記錄下來 並確認是否修過公民課 
                # 因為公民歷史都排在一起 所以只能判斷到最後一個公民課 (GQ456 為歷史課 ( 區域文明史 ) )
                i = i + 1 # 公民課的課程代碼
                category = '公民'
                while ( str( content[i] ) != 'GQ457' ) :
                    while ( str(content[i] ) == '' ) : # 把空格讀掉
                        i = i + 1 
                    course_code = str( content[i] ) # 課程代碼
                    i = i + 1 
                    course_name = str( content[i] ) # 課程名稱
                    i = i + 1
                    while ( str( content[i] ) == '' ) : # 把空格讀掉
                        i = i + 1
                    if ( str( content[i] ) in semester_list ) : # 有修過此堂課
                        semester = str( content[i] ) 
                        i = i + 1
                        course_code = str( content[i] )
                        i = i + 1
                        course_name = str( content[i] )
                        i = i + 1 # 性質: 半
                        i = i + 1 # 學期 下
                        i = i + 1 
                        credit = str( content[i] )
                        i = i + 1
                        score = str( content[i] )
                        
                        if ( score == '' ) : # 被當
                            fail_list.append( [course_code, category, course_name, credit] )
                        else : # 已修過
                            hasCivics = True 
                            course_list.append( [semester, course_code, category, course_name, credit, score] ) # 1082 GQ397 公民經濟學的世界 2 93
                    else : # 沒修過 此格會是0 代表0學分
                        civics_list.append( [course_code, category, course_name] ) # GQ397 公民 經濟學的世界
                        i = i + 1

                    if ( str( content[i] ) == '' ) : # 把空格讀掉
                        while ( str( content[i] ) == '' ) : 
                            i = i + 1
                    else : # 正常換下一個
                        i = i + 1 # 換下一個公民課
                # end while ( str( content[i] ) != 'GQ457' ) 將所有公民課記錄下來 並確認是否修過公民課
                

                hasHistory = False # 是否修過歷史課
                history_list = [] # 歷史課清單
                category = '歷史'
                # 目前的content[i] 是'GQ456' 為歷史課 ( 區域文明史 )
                while ( str( content[i] ) != '物類' ) : # 將所有歷史課記錄下來 並確認是否修過歷史課
                    while ( str(content[i] ) == '' ) : # 把空格讀掉
                        i = i + 1
                    course_code = str( content[i] ) # 課程代碼
                    i = i + 1 
                    course_name = str( content[i] ) # 課程名稱
                    i = i + 1
                    while ( str( content[i] ) == '' ) : # 把空格讀掉
                        i = i + 1
                    if ( str( content[i] ) in semester_list ) : # 有修過此堂課
                        semester = str( content[i] ) 
                        i = i + 1
                        course_code = str( content[i] )
                        i = i + 1
                        course_name = str( content[i] )
                        i = i + 1 # 性質: 半
                        i = i + 1 # 學期 下
                        i = i + 1 
                        credit = str( content[i] )
                        i = i + 1
                        score = str( content[i] )
                        
                        if ( score == '' ) : # 被當
                            fail_list.append( [course_code, category, course_name, credit] )
                        else : # 已修過
                            hasHistory = True 
                            course_list.append( [semester, course_code, category, course_name, credit, score] ) # 1082 GQ397 歷史 區域文明史 2 93
                    else : # 沒修過 此格會是0 代表0學分
                        history_list.append( [course_code, category, course_name] ) # GQ397 歷史 區域文明史
                        i = i + 1

                    if ( str( content[i] ) == '' ) : # 把空格讀掉
                        while ( str( content[i] ) == '' ) : 
                            i = i + 1
                    else : # 正常換下一個
                        i = i + 1 # 換下一個歷史課
                # end while ( str( content[i] ) != '物類' ) 將所有歷史課記錄下來 並確認是否修過歷史課

                
                # 因為目前條件讀到 ' 物類 ' 所以i不需要再加1
                
            # end elif ( stem == '人類' )
            elif ( stem == '物類' ) :
                wu_list = [] # 物類課程 list
                hasWu_basic = False # 是否修過物類的課程(被當則為False)
                
                i = i + 1 # 物類的課程代碼
                category = '基礎物類'
                while ( str( content[i] ) != '我類' ) :                
                    while ( str(content[i] ) == '' ) : # 把空格讀掉
                        i = i + 1 
                    course_code = str( content[i] ) # 課程代碼
                    i = i + 1 
                    course_name = str( content[i] ) # 課程名稱
                    i = i + 1
                    while ( str( content[i] ) == '' ) : # 把空格讀掉
                        i = i + 1
                    if ( str( content[i] ) in semester_list ) : # 有修過此堂課
                        semester = str( content[i] ) 
                        i = i + 1
                        course_code = str( content[i] )
                        i = i + 1
                        course_name = str( content[i] )
                        i = i + 1 # 性質: 半
                        i = i + 1 # 學期 下
                        i = i + 1 
                        credit = str( content[i] )
                        i = i + 1
                        score = str( content[i] )
                        
                        if ( score == '' ) : # 被當
                            fail_list.append( [course_code, category, course_name, credit] )
                        else : # 已修過
                            hasWu_basic = True 
                            course_list.append( [semester, course_code, category, course_name, credit, score] ) # 1082 GQ397 經濟學的世界 2 93
                    else : # 沒修過 此格會是0 代表0學分
                        wu_list.append( [course_code, category, course_name] ) # GQ397 經濟學的世界
                        i = i + 1

                    if ( str( content[i] ) == '' ) : # 把空格讀掉
                        while ( str( content[i] ) == '' ) : 
                            i = i + 1
                    else : # 正常換下一個
                        i = i + 1 # 換下一個物類課程
                # end while ( str( content[i] ) != '我類' ) 將所有物類課程記錄下來 並確認是否修過物類課程
                
            # end elif ( stem == '物類' ) 
            elif ( stem == '我類' ) :
                wo_list = [] # 物類課程 list
                hasWo_basic = False # 是否修過物類的課程(被當則為False)
                
                i = i + 1 # 我類的課程代碼
                category = '基礎我類'
                while ( str( content[i] ) != '通識基礎必修' ) :
                    while ( str(content[i] ) == '' ) : # 把空格讀掉
                        i = i + 1 
                    course_code = str( content[i] ) # 課程代碼
                    i = i + 1 
                    course_name = str( content[i] ) # 課程名稱
                    i = i + 1
                    while ( str( content[i] ) == '' ) : # 把空格讀掉
                        i = i + 1
                    if ( str( content[i] ) in semester_list ) : # 有修過此堂課
                        semester = str( content[i] ) 
                        i = i + 1
                        course_code = str( content[i] )
                        i = i + 1
                        course_name = str( content[i] )
                        i = i + 1 # 性質: 半
                        i = i + 1 # 學期 下
                        i = i + 1 
                        credit = str( content[i] )
                        i = i + 1
                        score = str( content[i] )
                        
                        if ( score == '' ) : # 被當
                            fail_list.append( [course_code, category, course_name, credit] )
                        else : # 已修過
                            hasWo_basic = True
                            course_list.append( [semester, course_code, category, course_name, credit, score] ) # 1082 GQ397 經濟學的世界 2 93
                    else : # 沒修過 此格會是0 代表0學分
                        wo_list.append( [course_code, category, course_name] ) # GQ397 經濟學的世界
                        i = i + 1

                    if ( str( content[i] ) == '' ) : # 把空格讀掉
                        while ( str( content[i] ) == '' ) : 
                            i = i + 1
                    else : # 正常換下一個
                        i = i + 1 # 換下一個物類課程
                # end while ( str( content[i] ) != '我類' ) 將所有物類課程記錄下來 並確認是否修過物類課程            
            # end elif ( stem == '我類' ) 

                # 目前 content[i] 為 "通識基礎必修"
                i = i + 1
                total_credit = str( content[i] ) # 通識基礎必修 總學分
                i = i + 1 
                while ( str( content[i] ) == '' ) :
                    i = i + 1 
                your_total_credit = str( content[i] ) # 已修學分  
                query['基礎通識總學分'] = total_credit   
                query['基礎通識學分_已得'] = your_total_credit
                query['基礎通識_已修'] = course_list
                # print( "-------------------------------------------------------")
                query['基礎通識_未修'] = must_list
                query['基礎通識_被當'] = fail_list
            elif ( stem == '天學' ) :
                category = '延伸天'
                hasTain = False # 是否有修過天類
                i = i + 1 
                while( str( content[i] ) == '' ) :
                    i = i + 1
                stem = str( content[i])
                if ( str( content[i] ) in semester_list ) : # 有修過此堂課
                    while ( stem != '人學' and stem != '物學'and stem != '我學' and stem != '通識延伸選修：各類至少修2學分,修滿14學分' ) :
                        semester = str( content[i] ) # 學期 1092
                        i = i + 1 
                        course_code = str( content[i] ) # 課程代碼
                        i = i + 1
                        course_name = str( content[i] ) # 課程名稱
                        i = i + 1 # 半
                        i = i + 1 # 上
                        i = i + 1
                        credit = str( content[i] ) # 學分
                        i = i + 1
                        score = str( content[i] ) # 分數
                        if ( score == '' ) : # 被當 
                            fail_list.append( [course_code, category, course_name, credit] )  
                        else : # 已修過天
                            hasTain = True
                            elective_counter = elective_counter + 1 # 計算已修過多少延伸通識選修
                            elective_course_list.append([semester, course_code, category, course_name, credit, score])
                        i = i + 1 # 換下一筆資料
                        while( str( content[i] ) == '' ) :
                            i = i + 1
                        stem = str( content[i])
                else:
                    i = i + 1
                    stem = str( content[i])
                # end while( stem != '人學' and stem != '物學'and stem != '我學' and stem != '通識延伸選修：各類至少修2學分,修滿14學分' )
            # end elif ( stem == '天學' ) 
            elif ( stem == '人學' ) :
                category = '延伸人'
                hasRen = False # 是否有修過人類
                i = i + 1 
                while( str( content[i] ) == '' ) :
                    i = i + 1   
                stem = str( content[i])
                if ( str( content[i] ) in semester_list ) : # 有修過此堂課
                    while ( stem != '物學'and stem != '我學' and stem != '通識延伸選修：各類至少修2學分,修滿14學分' ) :
                        semester = str( content[i] ) # 學期 1092
                        i = i + 1 
                        course_code = str( content[i] ) # 課程代碼
                        i = i + 1
                        course_name = str( content[i] ) # 課程名稱
                        i = i + 1 # 半
                        i = i + 1 # 上
                        i = i + 1
                        credit = str( content[i] ) # 學分
                        i = i + 1
                        score = str( content[i] ) # 分數
                        if ( score == '' ) : # 被當
                            fail_list.append( [course_code, category, course_name, credit] )  
                        else : # 已修過人
                            hasRen = True
                            elective_counter = elective_counter + 1 # 計算已修過多少延伸通識選修
                            elective_course_list.append([semester, course_code, category, course_name, credit, score])
                        i = i + 1 # 換下一筆資料
                        while( str( content[i] ) == '' ) :
                            i = i + 1
                        stem = str( content[i])
                else:
                    i = i + 1
                    stem = str( content[i])
                # end while  ( stem != '物學'and stem != '我學' and stem != '通識延伸選修：各類至少修2學分,修滿14學分' )
            # end elif ( stem == '人學' ) 
            elif ( stem == '物學' ) :
                category = '延伸物'
                hasWu = False # 是否有修過物類
                i = i + 1
                while( str( content[i] ) == '' ) :
                    i = i + 1
                stem = str( content[i])
                if ( str( content[i] ) in semester_list ) :  # 有修過此堂課
                    while ( stem != '我學' and stem != '通識延伸選修：各類至少修2學分,修滿14學分' ) :
                        semester = str( content[i] ) # 學期 1092
                        i = i + 1 
                        course_code = str( content[i] ) # 課程代碼
                        i = i + 1
                        course_name = str( content[i] ) # 課程名稱
                        i = i + 1 # 半
                        i = i + 1 # 上
                        i = i + 1
                        credit = str( content[i] ) # 學分
                        i = i + 1
                        score = str( content[i] ) # 分數
                        if ( score == '' ) : # 被當 
                            fail_list.append( [course_code, category, course_name, credit] )  
                        else : # 已修過物
                            hasWu = True
                            elective_counter = elective_counter + 1 # 計算已修過多少延伸通識選修
                            elective_course_list.append([semester, course_code, category, course_name, credit, score])
                        i = i + 1 # 換下一筆資料
                        while( str( content[i] ) == '' ) :
                            i = i + 1
                        stem = str( content[i])
                else:
                    i = i + 1
                    stem = str( content[i])
                # end while ( stem != '我學' and stem != '通識延伸選修：各類至少修2學分,修滿14學分' ) :
            # end elif ( stem == '物學' ) 
            elif ( stem == '我學' ) :
                category = '延伸我'
                hasWo = False # 是否有修過我類
                i = i + 1
                while( str( content[i] ) == '' ) :
                    i = i + 1 
                stem = str( content[i])
                if ( str( content[i] ) in semester_list ) : # 有修過此堂課
                    while ( stem != '通識延伸選修：各類至少修2學分,修滿14學分' ) :
                        semester = str( content[i] ) # 學期 1092
                        i = i + 1 
                        course_code = str( content[i] ) # 課程代碼
                        i = i + 1
                        course_name = str( content[i] ) # 課程名稱
                        i = i + 1 # 半
                        i = i + 1 # 上
                        i = i + 1
                        credit = str( content[i] ) # 學分
                        i = i + 1
                        score = str( content[i] ) # 分數
                        if ( score == '' ) : # 被當
                            fail_list.append( [course_code, category, course_name, credit] )  
                        else : # 已修過我
                            hasWo = True
                            elective_counter = elective_counter + 1 # 計算已修過多少延伸通識選修
                            elective_course_list.append([semester, course_code, category, course_name, credit, score])
                        i = i + 1 # 換下一筆資料
                        while( str( content[i] ) == '' ) :
                            i = i + 1
                        stem = str( content[i])
                else:
                    i = i + 1
                    stem = str( content[i])
                # end  while ( stem != '通識延伸選修：各類至少修2學分,修滿14學分' ) :
            # end elif ( stem == '我學' ) 
            elif ( str(content[i]) == '通識延伸選修：各類至少修2學分,修滿14學分' ):
                i = i + 1
                total_credit_elective = str( content[i] )
                i = i + 1
                while ( str(content[i]) == '' ) :
                    i = i + 1
                your_total_credit_elective = str( content[i] ) 
                query['延伸通識總學分'] = total_credit_elective
                query['延伸通識學分_已得'] = your_total_credit_elective 
                query['延伸通識_已修'] = elective_course_list
                query['延伸通識_被當'] = fail_list
                # if ( total_credit_elective <= your_total_credit_elective ) : 
                #     print( '恭喜已完成通識延伸選修' )
                # else :
                temp_counter = 0 
                query['延伸_天'] = hasTain
                query['延伸_人'] = hasRen
                query['延伸_物'] = hasWu
                query['延伸_我'] = hasWo
                if ( hasTain == False ) :
                    print( '延伸_天 還沒修唷 ')
                    temp_counter = temp_counter + 1
                if ( hasRen == False ) :
                    print( '延伸_人 還沒修唷 ')
                    temp_counter = temp_counter + 1
                if ( hasWu == False ) :
                    print( '延伸_物 還沒修唷 ')
                    temp_counter = temp_counter + 1
                if ( hasWo == False ) :
                    print( '延伸_我 還沒修唷 ')
                    temp_counter = temp_counter + 1

                numOfCourse = int(total_credit_elective) - int(your_total_credit_elective)
                if ( hasTain and hasRen and hasWu and hasWo ) :
                    numOfCourse = int(total_credit_elective) - int(your_total_credit_elective) 
                    numOfCourse = numOfCourse / 2 
                    query['延伸通識_未修'] = int(numOfCourse)
                    # print( '可以從延伸_天、人、物、我 中任選 ', int(numOfCourse) , ' 門課唷' )
                else :
                    temp_num = numOfCourse - temp_counter
                    if ( temp_num != 0 ) :
                        query['延伸通識_未修'] = temp_counter + temp_num
                        # print( '除了上述，還要再從延伸_天、人、物、我 中任選 ', temp_num , ' 門課唷' )

                i = i + 1 # 換下一筆資料
            # end elif ( str(content[i]) == '通識延伸選修：各類至少修2學分,修滿14學分' )
            elif ( stem == '學系必修' ) :
                course_list = []
                fail_list = []
                must_list = []
                done_required = True # 是否已修完必修課
                isFail = False # 是否被當
                category = '必修'
                i = i + 1
                while ( str( content[i] ) != '以上必修類別各課程學分數相加' ) :
                    if content[i] in semester_list: # 有修過此堂課
                        while(str( content[i] ) != '以上必修類別各課程學分數相加'):
                            i = i + 1
                        i = i - 1
                    else:
                        course_code = str( content[i] ) # 課程代碼
                        i = i + 1
                        course_name = str( content[i] ) # 課程名稱
                        i = i + 1
                        credit = str( content[i] ) # 學分數
                        i = i + 1
                        if ( str( content[i] ) not in semester_list ) : # 尚未修過
                            # done_required = False
                            # must_list.append( [course_code, category, course_name, credit] )
                            # while( str( content[i] ) == '' ) : # 把空白讀掉
                            i = i + 6
                        else : # 已修過此課程
                            semester = str( content[i] ) # 學期 1092
                            i = i + 1
                            course_code = str( content[i] ) # 課程代碼
                            i = i + 1
                            course_name = str( content[i] ) # 課程名稱
                            i = i + 1 # 半
                            i = i + 1 # 上
                            i = i + 1 
                            credit = str( content[i] ) # 學分數
                            i = i + 1
                            score = str( content[i] ) # 分數
                            if ( score == '' ) : # 被當
                                done_required = False
                                isFail = True
                                fail_list.append( [course_code, category, course_name, credit] )  
                            else :
                                course_list.append([semester, course_code, category, course_name, credit, score])
                        
                    i = i + 1 # 讀下筆資料
                    # while( str( content[i] ) == '' ) :
                    #     i = i + 1
                # end while( str( content[i] ) != '以上必修類別各課程學分數相加' ) :
                i = i + 1

                while ( str( content[i]) == '' ) : # 把空白讀掉
                    i = i + 1
                total_credit = str( content[i] )         
                query['必修學分_已得'] = total_credit
                query['必修_已修'] = course_list
                query['必修_未修'] = must_list
                query['必修_被當'] = fail_list
                i = i + 1 # 讀下筆資料
            # end elif ( str( conttent[i] ) ) == '學系必修' )
            elif ( stem == '學系選修' ) :
                course_list = []
                fail_list = []
                i = i + 1
                while ( str( content[i] ) == '' ) : # 空白讀掉
                    i = i + 1
                while ( str(content[i]) != '學系選修') :
                    if ( str( content[i] ) not in semester_list ) : # 未修過任何系選
                        total_credit_elective = str( content[i] )
                        i = i + 1
                        while ( str( content[i] ) == '' ) : # 空白讀掉
                            i = i + 1
                        your_total_credit_elective = str( content[i] )
                        query['系選總學分'] = total_credit_elective
                        query['系選學分_已得'] = your_total_credit_elective
                    else : # 有修過任一門系選
                        isFail = False 
                        semester = str( content[i] ) # 學期
                        i = i + 1
                        course_code = str( content[i] ) # 課程代碼
                        i = i + 1
                        course_name = str( content[i] ) # 課程名稱
                        i = i + 1 # 半
                        i = i + 1 # 上
                        i = i + 1 
                        credit = str( content[i] ) # 學分數
                        i = i + 1 
                        score = str( content[i]) # 分數
                        if ( score == '' ) : # 被當
                            isFail = True
                            fail_list.append( [course_code, category, course_name, credit] )  
                        else :
                            course_list.append([semester, course_code, category, course_name, credit, score])
                        i = i + 1 # 學系選修
                    while ( str( content[i] ) == '' ) : # 空白讀掉
                        i = i + 1
                # end while( str(content[i]) != '學系選修' ) 
                i = i + 1
                total_credit_elective = str( content[i] ) # 總系選學分
                i = i + 1
                while ( str( content[i] ) == '' ) : # 空白讀掉
                    i = i + 1
                your_total_credit_elective = str( content[i] ) # 已修系選學分
                query['系選總學分'] = total_credit_elective
                query['系選學分_已得'] = your_total_credit_elective
                left_credit = int( int(total_credit_elective) - int(your_total_credit_elective) ) # 還剩多少學分沒修
                query['系選_已修'] = course_list
                query['系選_被當'] = fail_list
                i = i + 1 # 讀下一筆資料   
            # end ( str( content[i]  ) == '學系選修' )
            elif ( stem == '非應修科目表中規定項目' ) :
                i = i + 1
                while ( str(content[i]) != '英文檢定' ) :
                    i = i + 1 
            # end elif ( stem == '非應修科目表中規定項目' ) 
            elif ( stem == '英文檢定' ) :
                i = i + 1
                if ( str( content[i]) == '通過' ) :
                    query['英文檢定'] = True
                else :
                    query['英文檢定'] = False
                i = i + 1 # 讀下一筆資料
            # end elif ( stem == '英文檢定' )
            elif ( stem == '本學系畢業應修最低學分數' ) :
                i = i + 1
                total_credit = str( content[i] ) 
                i = i + 1 # 學生已修畢本學系課程總學分數 ：
                i = i + 1 
                your_total_credit = str( content[i] ) 
                query['畢業所需學分數'] = total_credit
                query['畢業學分數_已得'] = your_total_credit
                break 
            # end elif( stem == '畢業應修最低學分數：' ) 
            elif (stem == '英語修課認證等級'):
                i = i + 1
                while( str(content[i]) != '課綱' ):
                    i = i + 1
                
            else :
                i = i + 1   
    # query['所有修習課程'] = query['必修_已修'] + query['延伸通識_已修'] + query['基礎通識_已修'] + query['基本知能_已修'] + query['系選_已修']
    # collection = db['存已修課程']
    # del_query = { 'UserID' : id }
    # collection.delete_many( del_query )
    # class_list = ClassLearned.GetMySelf( UserID, UserPasswd )
    # temp1 = []
    # temp2 = []
    # temp3 = []
    # temp4 = []
    # temp5 = []
    # for s in class_list :
    #     temp1.append(s[0])
    #     temp2.append(s[1])
    #     temp3.append(s[2])
    #     temp4.append(s[3])
    #     temp5.append(s[4])
    # query_insert = { 'UserID' : id, '學號' : UserID, '課程年分' : temp1, '課程代碼' : temp2, '課程名稱' : temp3, '學分' : temp4, '分數' : temp5 }
    # collection.insert_one( query_insert )

    return query