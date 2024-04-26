import matplotlib.pyplot as plt
import pandas as pd
from random import choice #隨機取配色用



pale_pink = "#fdc1c5" #粉色
wheat_yello = "#fbdd7e" #黃色
soft_blue = "#6488ea" # 藍1
light_periwinkle = "#c1c6fc" #藍2 (淺藍
periwinkle = "#8182fe" #藍3



paint_chip = []
paint_chip.append(["#bfc8d7", "#c2d2d2", "#e3e2b4", "#a2b59f", "#a2b59f"]) #配色表0  藍綠 上午/ 下午/ 晚上/ row/ col
paint_chip.append(["#f0e4d4", "#f9d9ca", "#d18063", "#fdc1c5", "#fdc1c5"]) #配色表1  粉
paint_chip.append(["#FDF2F0", "#F8DAE2", "#B57FB3", "#DEB3CF", "#DEB3CF"]) #配色表2  紫
paint_chip.append(["#E1F1E7", "#B1D3C5", "#CFDD8E", "#c7d6d8", "#c7d6d8"]) #配色表3  淺藍綠
paint_chip.append(["#ffc72c", "#fbdd7e", "#ffff81", "#da291c", "#da291c"]) #配色表4 麥當勞配色 好醜 
paint_chip.append(["#e4e4e4", "#e4e4e4", "#c6d3de", "#bb7059", "#cccc99"]) #配色表5 學校課表配色
paint_chip.append(["#fbdd7e", "#fffcc4", "#fbdd7e", "#ffc72c", "#ffc72c"]) #配色表6 黃 
paint_chip.append(["#E4A99B", "#E4A99B", "#E4A99B", "#838BB2", "#CACFE3"]) #配色表7 藍粉橘 
paint_chip.append(["#bfc8d7", "#c2d2d2", "#E4A99B", "#838BB2", "#CACFE3"]) #配色表8 藍綠偏藍 
paint_chip.append(["#fff3cd", "#fde4d6", "#fff3cd", "#dceaf5", "#dceaf5"]) #配色表9 淺藍黃粉
paint_chip.append(["#fff3cd", "#fde4d6", "#fff3cd", "#838BB2", "#838BB2"]) #配色表10 深藍黃粉  
paint_chip.append(["#e5dfed", "w", "#e5dfed", "#8165a2", "#8165a2"]) #配色表11 紫色條紋 
paint_chip.append(["#fdebc7", "#fdebc7", "#fdebc7", "#f4bc63", "#f4bc63"]) #配色表12 黃橘色
# num = 12







def set_color_sport(data, table_pd, title): # 體育課程表格˙設定顏色
    select_paint_chip = choice(paint_chip)
    row_col_color = select_paint_chip[3:5]  #選擇 行標籤列標籤顏色
    select_color = select_paint_chip[0:3] #選擇 元素顏色
    random_num = choice([0,1])
    
    fig, ax =plt.subplots(1,1)

    length_of_data = len(data) # 查到多少筆資料 
 
    column_labels=['課程代碼', '課程名稱', '授課導師', '時間', ' 備註']
    row_labels = []
    colors = []
    for i in range (0, length_of_data ) :
        row_labels.append(str(i+1))
        colors.append(["w","w","w","w","w"])


    for i in range ( 0, length_of_data ) : # 最多1~10
        for j in range ( 0, 5 ) : #   課程代碼      課程名稱 授課導師    時間      備註
            if ( data[i][j] != " " ): #有課就填入顏色
                colors[i][j] = select_color[random_num]
                 
            if ( j == 4 and data[i][j] != "無" ) :
                if select_color[random_num] == select_color[2] :
                    colors[i][j] = periwinkle
                else :
                    colors[i][j] = select_color[2]
              

    ax.set_title( label = title, loc = 'left' )
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText = table_pd.values,
            colLabels=column_labels,
            rowLabels=row_labels,
            rowColours = [row_col_color[random_num]] * length_of_data,  
            colColours =[row_col_color[random_num]] * 5,
            loc="center",
            cellColours = colors )

    return ax.table

def set_color(data, table_pd, title): # 一般課表 設定顏色

    numbers_list = []
    for i in range (0, len(paint_chip) ) : # 隨機挑選做條紋
        numbers_list.append(i)

    random_num = choice(numbers_list) # 隨機挑選做條紋

    select_paint_chip = choice(paint_chip)

    # number_of_paint_chip = num # 測試用
    # select_paint_chip = paint_chip[num] # 測試用


    row_col_color = select_paint_chip[3:5] #選擇 行標籤列標籤顏色
    select_color = select_paint_chip[0:3] #選擇 元素顏色

    fig, ax =plt.subplots(1,1)
    column_labels=['週一', '週二', '週三', '週四', '週五', '週六', '週日' ]
    row_labels = ['07:10~\n08:00    A', '08:10~\n09:00    1', '09:10~\n10:00    2', '10:10~\n11:00    3', '11:10~\n12:00    4', '12:10~\n13:00    B', '13:10~\n14:00    5', '14:10~\n15:00    6', '15:10~\n16:00    7', '16:10~\n17:00    8', '17:05~\n17:55    C', '18:00~\n18:50    D', '18:55~\n19:45    E', '19:50~\n20:40    F', '20:45~\n21:35    G']
    colors = [["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
              ["w","w","w","w","w","w","w"],
            ]

    # 以下為配色
    for i in range ( 0, 15 ) : # 第幾節課
        for j in range ( 0, 7 ) : # 禮拜幾(一~日)
            if ( select_paint_chip == paint_chip[5] ) : # 學校特殊配色才用
                    
                if ( i == 0 or i == 5 ) :
                    colors[i][j] = select_color[2] 
                else :
                    colors[i][j] = select_color[0]

            elif ( select_paint_chip == paint_chip[11] or select_paint_chip == paint_chip[random_num] ) : # 條紋設計
               if ( i%2 == 1 ) :
                    colors[i][j] = select_color[0]
                    if ( select_color[1] == select_color[0] ) :
                        colors[i][j] = "w"
               else :
                    colors[i][j] = select_color[1]
 
            
            elif ( data[i][j] != " " ): #有課就填入顏色 (非學校配色)
 
                if ( i < 5 ) :
                     colors[i][j] = select_color[0]   
                elif ( i > 4 and i < 10 ) :
                    colors[i][j] = select_color[1] 
                    temp_str = data[i][j]
                else :
                    if ( data[i][j] == data[9][j] ) :
                        colors[i][j] = select_color[1] 
                    else :
                        colors[i][j] = select_color[2] 
                


    ax.set_title( label = title, loc = 'left' )
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText = table_pd.values,
            colLabels=column_labels,
            rowLabels=row_labels,
            rowColours = [row_col_color[0]] * 15,  
            colColours =[row_col_color[1]] * 7,
            loc="center",
            cellColours = colors )



    return ax.table