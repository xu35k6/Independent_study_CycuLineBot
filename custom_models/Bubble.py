# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 18:47:09 2020

@author: LIN
"""
#一個BUBBLE的字典
#用來製作Flex Message
#type1-->只有1個時間段 2就是2個時間...
from cgitb import reset
from unittest import result


Bubble_Type_1 =     {
  "type": "bubble",
  "hero": {
    "type": "box",
    "layout": "vertical",
    "contents": []
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "課程名稱",
        "weight": "bold",
        "size": "xl",
        "margin": "md",
        "align": "start"
      },
	  {
        "type": "text",
        "text": "課程類別",
        "align": "start"
      },
      {
        "type": "text",
        "text": "授課老師",
        "align": "start"
      },
      {
        "type": "text",
        "text": "上課時間地點",
        "align": "start"
      }
    ],
    "backgroundColor": "#e6f2ff"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "加入我的課表",
          "data": "加入我的課表"
        }
      }
    ]
  }
}

Bubble_Type_2 =     {
  "type": "bubble",
  "hero": {
    "type": "box",
    "layout": "vertical",
    "contents": []
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "課程名稱",
        "weight": "bold",
        "size": "xl",
        "margin": "md",
        "align": "start"
      },
	  {
        "type": "text",
        "text": "課程類別",
        "align": "start"
      },
      {
        "type": "text",
        "text": "授課老師",
        "align": "start"
      },
      {
        "type": "text",
        "text": "上課時間地點1",
        "align": "start"
      },
      {
        "type": "text",
        "text": "上課時間地點2"
      }
    ],
    "backgroundColor": "#e6f2ff"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "加入我的課表",
          "data": "加入我的課表"
        }
      }
    ]
  }
}

Bubble_Type_3 =     {
  "type": "bubble",
  "hero": {
    "type": "box",
    "layout": "vertical",
    "contents": []
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "課程名稱",
        "weight": "bold",
        "size": "xl",
        "margin": "md",
        "align": "start"
      },
	  {
        "type": "text",
        "text": "課程類別",
        "align": "start"
      },
      {
        "type": "text",
        "text": "授課老師",
        "align": "start"
      },
      {
        "type": "text",
        "text": "上課時間地點1",
        "align": "start"
      },
      {
        "type": "text",
        "text": "上課時間地點2"
      },
      {
        "type": "text",
        "text": "上課時間地點3"
      }
    ],
    "backgroundColor": "#e6f2ff"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "加入我的課表",
          "data": "加入我的課表"
        }
      }
    ]
  }
}

#一個BUBBLE的字典
#用來製作Flex Message
Bubble_Type =     {
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
            "margin": "none",
            "size": "full",
            "aspectMode": "cover",
            "animated": True
          }
        ],
        "backgroundColor": "#D0D0D0"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "搜尋結果",
            "size": "xl",
            "weight": "bold",
            "position": "relative",
            "align": "center",
            "wrap": True,
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "http://linecorp.com/"
            }
          }
        ],
        "paddingTop": "none",
        "backgroundColor": "#D0D0D0"
      }
    }


Bubble_Scholarship_Type =    {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "justifyContent": "center",
    "contents": [
      {
        "type": "text",
        "text": "這是獎學金標題",
        "size": "xl",
        "position": "relative",
        "weight": "bold",
        "wrap": True,
        "align": "center"
      }
    ],    
    "height": "100px",
    "backgroundColor": "#D0D0D0",
    "background": {
        "type": "linearGradient",
        "angle": "0deg",
        "endColor": "#9D9D9D",
        "startColor": "#F0F0F0"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "截止日期",
        "size": "xl",
        "margin": "none"
      },
      {
        "type": "text",
        "text": "金額",
        "size": "xl",
        "margin": "md"
      },
      {
        "type": "button",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/",
          "label": "點我領錢"
        },
        "style": "primary",
        "position": "relative",
        "margin": "xxl",
        "height": "md",
        "offsetTop": "xs"
      }
    ],
    "backgroundColor": "#F0F0F0"
  }
}
def Bubble_mid_distance(itinerary,i):
  bubble_mid_distance = {
    "type": "bubble",
    "size": "mega",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        # {
        #   "type": "image",
        #   "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #   "margin": "none",
        #   "position": "absolute",
        #   "offsetTop": "none",
        #   "gravity": "center",
        #   "aspectMode": "cover",
        #   "offsetStart": "none",
        #   "offsetBottom": "none",
        #   "offsetEnd": "none",
        #   "size": "full"
        # },
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "從",
              "color": "#ffffff66",
              "size": "sm"
            },
            {
              "type": "text",
              "text": itinerary.origin_station[i],
              "color": "#ffffff",
              "size": "xl",
              "flex": 4,
              "weight": "bold",
              "action": {
                "type": "uri",
                "label": "action",
                "uri": "http://linecorp.com/"
              }
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": '搭乘',
              "color": "#ffffff66",
              "size": "sm"
            },
            {
              "type": "text",
              "text": itinerary.route_name[i]+'號:'+itinerary.time[i],
              "color": "#ffffff",
              "size": "xl",
              "flex": 4,
              "weight": "bold"
            }
          ]
        }
      ],
      "paddingAll": "20px",
      "backgroundColor": "#0367D3",
      "spacing": "md",
      "height": "154px",
      "paddingTop": "22px",
      "background": {
        "type": "linearGradient",
        "angle": "0deg",
        "startColor": "#000000",
        "endColor": "#ffffff"
      }
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": '方案'+str(i+1),
          "color": "#b7b7b7",
          "size": "xs"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "text",
              "text": "當前",
              "size": "sm",
              "gravity": "center"
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "filler"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [],
                  "cornerRadius": "30px",
                  "height": "12px",
                  "width": "12px",
                  "borderColor": "#EF454D",
                  "borderWidth": "2px"
                },
                {
                  "type": "filler"
                }
              ],
              "flex": 0
            },
            {
              "type": "text",
              "text": "起點",
              "gravity": "center",
              "flex": 4,
              "size": "sm"
            }
          ],
          "spacing": "lg",
          "cornerRadius": "30px",
          "margin": "xl"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "box",
              "layout": "baseline",
              "contents": [
                {
                  "type": "filler"
                }
              ],
              "flex": 1
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "filler"
                    },
                    {
                      "type": "box",
                      "layout": "vertical",
                      "contents": [],
                      "width": "2px",
                      "backgroundColor": "#B7B7B7"
                    },
                    {
                      "type": "filler"
                    }
                  ],
                  "flex": 1
                }
              ],
              "width": "12px"
            },
            {
              "type": "text",
              "text": '步行'+itinerary.walk_dis_1[i]+'公尺',
              "gravity": "center",
              "flex": 4,
              "size": "xs",
              "color": "#8c8c8c"
            }
          ],
          "spacing": "lg",
          "height": "64px"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": '起點站',
                  "gravity": "center",
                  "size": "sm"
                }
              ],
              "flex": 1
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "filler"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [],
                  "cornerRadius": "30px",
                  "width": "12px",
                  "height": "12px",
                  "borderWidth": "2px",
                  "borderColor": "#6486E3"
                },
                {
                  "type": "filler"
                }
              ],
              "flex": 0
            },
            {
              "type": "text",
              "text": itinerary.origin_station[i],
              "gravity": "center",
              "flex": 4,
              "size": "sm"
            }
          ],
          "spacing": "lg",
          "cornerRadius": "30px"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "box",
              "layout": "baseline",
              "contents": [
                {
                  "type": "filler"
                }
              ],
              "flex": 1
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "filler"
                    },
                    {
                      "type": "box",
                      "layout": "vertical",
                      "contents": [],
                      "width": "2px",
                      "backgroundColor": "#6486E3"
                    },
                    {
                      "type": "filler"
                    }
                  ],
                  "flex": 1
                }
              ],
              "width": "12px"
            },
            {
              "type": "text",
              "text": '經過'+itinerary.stop_num[i]+'站',
              "gravity": "center",
              "flex": 4,
              "size": "xs",
              "color": "#8c8c8c"
            }
          ],
          "spacing": "lg",
          "height": "64px"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "text",
              "text": "終點站",
              "gravity": "center",
              "size": "sm"
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "filler"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [],
                  "cornerRadius": "30px",
                  "width": "12px",
                  "height": "12px",
                  "borderColor": "#6486E3",
                  "borderWidth": "2px"
                },
                {
                  "type": "filler"
                }
              ],
              "flex": 0
            },
            {
              "type": "text",
              "text": itinerary.end_station[i],
              "gravity": "center",
              "flex": 4,
              "size": "sm"
            }
          ],
          "spacing": "lg",
          "cornerRadius": "30px"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "box",
              "layout": "baseline",
              "contents": [
                {
                  "type": "filler"
                }
              ],
              "flex": 1
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "filler"
                    },
                    {
                      "type": "box",
                      "layout": "vertical",
                      "contents": [],
                      "width": "2px",
                      "backgroundColor": "#6486E3"
                    },
                    {
                      "type": "filler"
                    }
                  ],
                  "flex": 1
                }
              ],
              "width": "12px"
            },
            {
              "type": "text",
              "text": '步行'+itinerary.walk_dis_2[i]+'公尺',
              "gravity": "center",
              "flex": 4,
              "size": "xs",
              "color": "#8c8c8c"
            }
          ],
          "spacing": "lg",
          "height": "64px"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "text",
              "text": "目的地",
              "gravity": "center",
              "size": "sm"
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "filler"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [],
                  "cornerRadius": "30px",
                  "width": "12px",
                  "height": "12px",
                  "borderColor": "#6486E3",
                  "borderWidth": "2px"
                },
                {
                  "type": "filler"
                }
              ],
              "flex": 0
            },
            {
              "type": "text",
              "text": "終點",
              "gravity": "center",
              "flex": 4,
              "size": "sm"
            }
          ],
          "spacing": "lg",
          "cornerRadius": "30px"
        }
      ],
      "spacing": "none"
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "導航至公車站",
            "uri": "https://www.google.com/maps/dir//"+ str(itinerary.log_lat[i])
          }
        }
      ]
    }
  }
  return bubble_mid_distance

def Bubble_bus(route,end_station,total_bubble,btn,color):
  result = {
    "type": "bubble",
    "size": "mega",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": str(route),
              "color": "#ffffff",
              "size": "xl",
              "flex": 4,
              "weight": "bold",
              "align": "center",
              "wrap": True
            }
          ]
        },
        {
          "type": "text",
          "text": end_station,
          "size": "xl",
          "align": "center",
          "color": "#ffff66"
        }
      ],
      "paddingAll": "20px",
      "backgroundColor": color,
      "spacing": "md",
      "paddingTop": "22px"
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": total_bubble
    },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": btn
  }
  }
  return result

def btn(location):
  
  result = {
    "type": "button",
    "action": {
      "type": "uri",
      "label": "導航",
      "uri": "https://www.google.com/maps/dir//"+ location
    },
    "style": "primary",
    "color": "#0367D3",
    "margin": "none"
  }
  return result
def make_bus_body_tittle(name):
  result = {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "text",
        "text": str(name),
        "gravity": "center",
        "flex": 4,
        "size": "lg"
      }
    ],
    "spacing": "lg",
    "cornerRadius": "30px"
  }
  return result
def make_bus_body(time):
  result = {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "filler"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "cornerRadius": "30px",
            "width": "12px",
            "height": "12px",
            "borderColor": "#6486E3",
            "borderWidth": "2px"
          },
          {
            "type": "filler"
          }
        ],
        "flex": 0
      },
      {
        "type": "text",
        "text": str(time),
        "gravity": "center",
        "flex": 4,
        "size": "sm",
        "color" : "#FFFFFF"
      }
    ],
    "spacing": "lg",
    "cornerRadius": "30px",
    "backgroundColor" : "#3C3C3C"
  }
  return result
def Bubble_bike(Return,Rent,name,google_map):
  result = {
    "type": "bubble",
    "size": "mega",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "YouBike",
              "color": "#ffffff",
              "size": "3xl",
              "flex": 4,
              "weight": "bold"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "站名:"+name,
              "color": "#ffffff",
              "flex": 4,
              "weight": "bold",
              "size": "md"
            }
          ]
        }
      ],
      "paddingAll": "20px",
      "backgroundColor": "#FF8000",
      "spacing": "md",
      "height": "120px",
      "paddingTop": "22px"
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "text",
              "text": "✯可租借車輛",
              "gravity": "center",
              "flex": 4,
              "size": "md"
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "filler"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [],
                  "cornerRadius": "xxl",
                  "width": "12px",
                  "height": "12px",
                  "borderWidth": "bold",
                  "borderColor": "#FF8000"
                },
                {
                  "type": "filler"
                }
              ],
              "flex": 0
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": str(Rent),
                  "size": "md"
                }
              ]
            }
          ],
          "spacing": "lg",
          "cornerRadius": "30px"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "text",
              "text": "✯可返車車位",
              "gravity": "center",
              "flex": 4,
              "size": "md"
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "filler"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [],
                  "cornerRadius": "30px",
                  "width": "12px",
                  "height": "12px",
                  "borderWidth": "bold",
                  "borderColor": "#FF8000"
                },
                {
                  "type": "filler"
                }
              ],
              "flex": 0
            },
            {
              "type": "text",
              "text": str(Return),
              "size": "md"
            }
          ],
          "spacing": "lg",
          "cornerRadius": "30px",
          "borderColor": "#FF8000"
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "separator",
          "color": "#000000"
        },
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "導航",
            "uri": str(google_map)
          },
          "gravity": "top"
        }
      ]
    }
  }
  return result
#將bubble合併成carousel
def make_carousel(bubble_total): 
  carousel = {
    "type": "carousel",
    "contents": bubble_total #[]
  }
  return carousel
def Train_area(tittle):
  train_area={
    "type": "bubble",
    "size": "giga",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "請選擇"+tittle+"地區",
          "size": "xxl",
          "color": "#ECF5FF"
        }
      ],
      "backgroundColor": "#0066CC"
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "臺北/基隆",
                "text": "臺北/基隆"
              },
              "style": "primary",
              "color": "#5A5AAD"
            },
            {
              "type": "separator",
              "margin": "sm"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "桃園",
                "text": "桃園"
              },
              "color": "#5A5AAD",
              "style": "primary"
            },
            {
              "type": "separator",
              "margin": "sm"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "新竹",
                "text": "新竹"
              },
              "color": "#5A5AAD",
              "style": "primary"
            }
          ],
          "borderColor": "#ECF5FF",
          "borderWidth": "normal"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "台東",
                "text": "台東"
              },
              "style": "primary",
              "color": "#7D7DFF"
            },
            {
              "type": "separator",
              "margin": "sm"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "花蓮",
                "text": "花蓮"
              },
              "color": "#7D7DFF",
              "style": "primary"
            },
            {
              "type": "separator",
              "margin": "sm"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "宜蘭",
                "text": "宜蘭"
              },
              "color": "#7D7DFF",
              "style": "primary"
            }
          ],
          "borderColor": "#ECF5FF",
          "borderWidth": "normal"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "苗栗",
                "text": "苗栗"
              },
              "style": "primary",
              "color": "#5A5AAD"
            },
            {
              "type": "separator",
              "margin": "sm"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "台中",
                "text": "台中"
              },
              "color": "#5A5AAD",
              "style": "primary"
            },
            {
              "type": "separator",
              "margin": "sm"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "彰化",
                "text": "彰化"
              },
              "color": "#5A5AAD",
              "style": "primary"
            }
          ],
          "borderColor": "#ECF5FF",
          "borderWidth": "normal"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "南投",
                "text": "南投"
              },
              "style": "primary",
              "color": "#7D7DFF"
            },
            {
              "type": "separator",
              "margin": "sm"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "雲林",
                "text": "雲林"
              },
              "color": "#7D7DFF",
              "style": "primary"
            },
            {
              "type": "separator",
              "margin": "sm"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "嘉義",
                "text": "嘉義"
              },
              "color": "#7D7DFF",
              "style": "primary"
            }
          ],
          "borderColor": "#ECF5FF",
          "borderWidth": "normal"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "台南",
                "text": "台南"
              },
              "style": "primary",
              "color": "#5A5AAD"
            },
            {
              "type": "separator",
              "margin": "sm"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "高雄",
                "text": "高雄"
              },
              "color": "#5A5AAD",
              "style": "primary"
            },
            {
              "type": "separator",
              "margin": "sm"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "屏東",
                "text": "屏東"
              },
              "color": "#5A5AAD",
              "style": "primary"
            }
          ],
          "borderColor": "#ECF5FF",
          "borderWidth": "normal"
        }
      ]
    }
  }
  return train_area
def Train_location(tittle,destination):
  train_location= { 
    '臺北/基隆':{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "臺北",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "南港",
                      "text": "南港"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "松山",
                      "text": "松山"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "萬華",
                      "text": "萬華"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "臺北",
                      "text": "臺北"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ]
              }
            ]
          }
        },
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "新北",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "五堵",
                      "text": "五堵"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "汐止",
                      "text": "汐止"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "汐科",
                      "text": "汐科"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "板橋",
                      "text": "板橋"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "text": "浮洲",
                      "label": "浮洲"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "樹林",
                      "text": "樹林"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "南樹林",
                      "text": "南樹林"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "山佳",
                      "text": "山佳"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "鶯歌",
                      "text": "鶯歌"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "福隆",
                      "text": "福隆"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "貢寮",
                      "text": "貢寮"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "雙溪",
                      "text": "雙溪"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "牡丹",
                      "text": "牡丹"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "三貂嶺",
                      "text": "三貂嶺"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大華",
                      "text": "大華"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "十分",
                      "text": "十分"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "望古",
                      "text": "望古"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "嶺腳",
                      "text": "嶺腳"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "平溪",
                      "text": "平溪"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "菁桐",
                      "text": "菁桐"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "猴硐",
                      "text": "猴硐"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "瑞芳",
                      "text": "瑞芳"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "八斗子",
                      "text": "八斗子"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "四腳亭",
                      "text": "四腳亭"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        },
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "基隆",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "基隆",
                      "text": "基隆"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "三坑",
                      "text": "三坑"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "八堵",
                      "text": "八堵"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "七堵",
                      "text": "七堵"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "百福",
                      "text": "百福"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "暖暖",
                      "text": "暖暖"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "海科館",
                      "text": "海科館"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                    }
                  ]
                }
              ]
            }
          }
        ]
      },
    '桃園':{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "桃園",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "桃園",
                      "text": "桃園"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "內壢",
                      "text": "內壢"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "中壢",
                      "text": "中壢"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "埔心",
                      "text": "埔心"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "楊梅",
                      "text": "楊梅"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "富岡",
                      "text": "富岡"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "新富",
                      "text": "新富"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ]
              }
            ]
          }
        }
      ]
    },
    "新竹":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "新竹縣",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "北湖",
                      "text": "北湖"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "湖口",
                      "text": "湖口"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "新豐",
                      "text": "新豐"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "竹北",
                      "text": "竹北"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "text": "竹中",
                      "label": "竹中"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "六家",
                      "text": "六家"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "上員",
                      "text": "上員"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "榮華",
                      "text": "榮華"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "竹東",
                      "text": "竹東"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "橫山",
                      "text": "橫山"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "九讚頭",
                      "text": "九讚頭"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "合興",
                      "text": "合興"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "富貴",
                      "text": "富貴"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "內灣",
                      "text": "內灣"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        },
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "新竹市",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "北新竹",
                      "text": "北新竹"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "千甲",
                      "text": "千甲"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "新莊",
                      "text": "新莊"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "新竹",
                      "text": "新竹"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "三姓橋",
                      "text": "三姓橋"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "香山",
                      "text": "香山"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ]
              }
            ]
          }
        }
      ]
    },
    "台東":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "台東",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大武",
                      "text": "大武"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "瀧溪",
                      "text": "瀧溪"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "金崙",
                      "text": "金崙"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "太麻里",
                      "text": "太麻里"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "text": "知本",
                      "label": "知本"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "康樂",
                      "text": "康樂"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "台東",
                      "text": "台東"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "山里",
                      "text": "山里"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "鹿野",
                      "text": "鹿野"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "瑞源",
                      "text": "瑞源"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "瑞和",
                      "text": "瑞和"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "關山",
                      "text": "關山"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "海端",
                      "text": "海端"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "池上",
                      "text": "池上"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    },
    "花蓮":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "花蓮",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "富里",
                      "text": "富里"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "東竹",
                      "text": "東竹"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "東里",
                      "text": "東里"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "玉里",
                      "text": "玉里"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "text": "三民",
                      "label": "三民"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "瑞穗",
                      "text": "瑞穗"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "富源",
                      "text": "富源"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大富",
                      "text": "大富"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "光復",
                      "text": "光復"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "萬榮",
                      "text": "萬榮"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "鳳林",
                      "text": "鳳林"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "南平",
                      "text": "南平"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "和平",
                      "text": "和平"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "豐田",
                      "text": "豐田"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "壽豐",
                      "text": "壽豐"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "平和",
                      "text": "平和"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "志學",
                      "text": "志學"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "吉安",
                      "text": "吉安"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "花蓮",
                      "text": "花蓮"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "北埔",
                      "text": "北埔"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "景美",
                      "text": "景美"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "新城",
                      "text": "新城"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "崇德",
                      "text": "崇德"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "和仁",
                      "text": "和仁"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "林榮新光",
                      "text": "林榮新光"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    },
    "宜蘭":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "宜蘭",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "漢本",
                      "text": "漢本"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "武塔",
                      "text": "武塔"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "南澳",
                      "text": "南澳"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "東澳",
                      "text": "東澳"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "text": "永樂",
                      "label": "永樂"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "蘇澳",
                      "text": "蘇澳"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "蘇澳新",
                      "text": "蘇澳新"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "冬山",
                      "text": "冬山"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "羅東",
                      "text": "羅東"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "中里",
                      "text": "中里"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "二結",
                      "text": "二結"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "宜蘭",
                      "text": "宜蘭"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "四城",
                      "text": "四城"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "礁溪",
                      "text": "礁溪"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "頂埔",
                      "text": "頂埔"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "頭城",
                      "text": "頭城"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "外澳",
                      "text": "外澳"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "龜山",
                      "text": "龜山"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大溪",
                      "text": "大溪"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大里",
                      "text": "大里"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "石城",
                      "text": "石城"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    },
    "苗栗":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "苗栗",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "崎頂",
                      "text": "崎頂"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "竹南",
                      "text": "竹南"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "談文",
                      "text": "談文"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大山",
                      "text": "大山"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "text": "後龍",
                      "label": "後龍"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "龍港",
                      "text": "龍港"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "白沙屯",
                      "text": "蘇澳新"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "新埔",
                      "text": "新埔"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "通霄",
                      "text": "通霄"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "苑裡",
                      "text": "苑裡"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "造橋",
                      "text": "造橋"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "豐富",
                      "text": "豐富"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "苗栗",
                      "text": "苗栗"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "南勢",
                      "text": "南勢"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "銅鑼",
                      "text": "銅鑼"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "三義",
                      "text": "三義"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    },
    "台中":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "台中",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "日南",
                      "text": "日南"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大甲",
                      "text": "大甲"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "台中港",
                      "text": "台中港"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "清水",
                      "text": "清水"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "text": "沙鹿",
                      "label": "沙鹿"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "龍井",
                      "text": "龍井"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大肚",
                      "text": "大肚"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "追分",
                      "text": "追分"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "泰安",
                      "text": "泰安"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "后里",
                      "text": "后里"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "豐原",
                      "text": "豐原"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "栗林",
                      "text": "栗林"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "潭子",
                      "text": "潭子"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "頭家厝",
                      "text": "頭家厝"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "松竹",
                      "text": "松竹"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "太原",
                      "text": "太原"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "精武",
                      "text": "精武"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "台中",
                      "text": "台中"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "五權",
                      "text": "五權"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大慶",
                      "text": "大慶"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "烏日",
                      "text": "烏日"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "新烏日",
                      "text": "新烏日"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "成功",
                      "text": "成功"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    },
    "彰化":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "彰化",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "彰化",
                      "text": "彰化"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "花壇",
                      "text": "花壇"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大村",
                      "text": "大村"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "員林",
                      "text": "員林"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "永靖",
                      "text": "永靖"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "社頭",
                      "text": "社頭"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "田中",
                      "text": "田中"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "二水",
                      "text": "二水"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "源泉",
                      "text": "源泉"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    },
    "南投":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "南投",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "濁水",
                      "text": "濁水"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "龍泉",
                      "text": "龍泉"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "集集",
                      "text": "集集"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "水里",
                      "text": "水里"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "車埕",
                      "text": "車埕"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    },
    "雲林":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "雲林",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "林內",
                      "text": "林內"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "石榴",
                      "text": "石榴"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "斗六",
                      "text": "斗六"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "斗南",
                      "text": "斗南"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "石龜",
                      "text": "石龜"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    },
    "嘉義":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "嘉義縣",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大林",
                      "text": "大林"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "民雄",
                      "text": "民雄"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "水上",
                      "text": "水上"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "南靖",
                      "text": "南靖"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        },
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "嘉義市",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "嘉北",
                      "text": "嘉北"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "嘉義",
                      "text": "嘉義"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    },
    "台南":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "台南",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "後壁",
                      "text": "後壁"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "text": "新營",
                      "label": "新營"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "柳營",
                      "text": "柳營"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "林鳳營",
                      "text": "林鳳營"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "隆田",
                      "text": "隆田"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "拔林",
                      "text": "拔林"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "善化",
                      "text": "善化"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "南科",
                      "text": "南科"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "新市",
                      "text": "新市"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "永康",
                      "text": "永康"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大橋",
                      "text": "大橋"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "台南",
                      "text": "台南"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "保安",
                      "text": "保安"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "仁德",
                      "text": "仁德"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "中洲",
                      "text": "中洲"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "長榮大學",
                      "text": "長榮大學"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "沙崙",
                      "text": "沙崙"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    },
    "高雄":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "高雄",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "大湖",
                      "text": "大湖"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "text": "路竹",
                      "label": "路竹"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "岡山",
                      "text": "岡山"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "橋頭",
                      "text": "橋頭"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "楠梓",
                      "text": "楠梓"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "新左營",
                      "text": "新左營"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "左營",
                      "text": "左營"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "內惟",
                      "text": "內惟"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "美術館",
                      "text": "美術館"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "鼓山",
                      "text": "鼓山"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "三塊厝",
                      "text": "三塊厝"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "高雄",
                      "text": "高雄"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "民族",
                      "text": "民族"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "科工館",
                      "text": "科工館"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "正義",
                      "text": "正義"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "鳳山",
                      "text": "鳳山"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "後庄",
                      "text": "後庄"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "九曲堂",
                      "text": "九曲堂"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    },
    "屏東":{
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "mega",
          "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "請選擇"+tittle,
                "size": "xl",
                "color": "#ECF5FF"
              },
              {
                "type": "text",
                "text": "屏東",
                "color": "#ECF5FF",
                "size": "xxl",
                "align": "center",
                "decoration": "underline"
              }
            ],
            "backgroundColor": "#0066CC"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "六塊厝",
                      "text": "六塊厝"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "text": "屏東",
                      "label": "屏東"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "歸來",
                      "text": "歸來"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "麟洛",
                      "text": "麟洛"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "西勢",
                      "text": "西勢"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "竹田",
                      "text": "竹田"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "潮州",
                      "text": "潮州"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "崁頂",
                      "text": "崁頂"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "南州",
                      "text": "南州"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "鎮安",
                      "text": "鎮安"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "林邊",
                      "text": "林邊"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "佳冬",
                      "text": "佳冬"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "東海",
                      "text": "東海"
                    },
                    "style": "primary",
                    "color": "#7D7DFF"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "枋寮",
                      "text": "枋寮"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "加祿",
                      "text": "加祿"
                    },
                    "color": "#7D7DFF",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "內獅",
                      "text": "內獅"
                    },
                    "style": "primary",
                    "color": "#5A5AAD"
                  },
                  {
                    "type": "separator",
                    "margin": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "枋山",
                      "text": "枋山"
                    },
                    "color": "#5A5AAD",
                    "style": "primary"
                  }
                ],
                "borderWidth": "normal"
              }
            ]
          }
        }
      ]
    }
  }
  return train_location[destination]
def train_information(information):
  origin = information[0]
  destination = information[1]
  route = information[2]
  delay = information[3]
  train_type = information[4]
  Departure_time = information[5]
  Arrival_time = information[6]
  remark = information[7]
  if train_type[0] == '自':
    coler = '#EA0000'
  elif train_type[0] == '普':
    coler = '#FF9224'	
  elif train_type[0] == '區':
    coler = '#4A4AFF'
  else:
    coler = '#8080C0'

  result = {
    "type": "bubble",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": str(route),
          "color": "#FFFFFF",
          "size": "xxl"
        },
        {
          "type": "text",
          "text": train_type,
          "color": "#FFFFFF",
          "size": "sm"
        }
      ]
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": origin+"➮"+destination,
          "size": "xs"
        },
        {
          "type": "separator"
        },
        {
          "type": "text",
          "text": str(Departure_time)+"➮"+str(Arrival_time),
          "size": "3xl",
          "weight": "bold",
          "align": "center"
        },
        {
          "type": "text",
          "text": str(delay),
          "align": "center"
        },
        {
          "type": "separator"
        },
        {
          "type": "text",
          "text": remark,
          "size": "xxs"
        }
      ]
    },
    "styles": {
      "header": {
        "backgroundColor": coler
      }
    }
  }
  return result

def train_route(route1,route2,route3,route4,route5):
  result={
    "type": "bubble",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "火車常用路線",
          "color": "#FFFFFF",
          "size": "3xl"
        }
      ]
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "message",
            "label": route1,
            "text": route1
          },
          "style": "primary",
          "color": "#009100"
        },
        {
          "type": "button",
          "action": {
            "type": "message",
            "label": route2,
            "text": route2
          },
          "style": "primary",
          "color": "#009100"
        },
        {
          "type": "button",
          "action": {
            "type": "message",
            "label": route3,
            "text": route3
          },
          "style": "primary",
          "color": "#009100"
        },
        {
          "type": "button",
          "action": {
            "type": "message",
            "label": route4,
            "text": route4
          },
          "color": "#009100",
          "style": "primary"
        },
        {
          "type": "button",
          "action": {
            "type": "message",
            "label": route5,
            "text": route5
          },
          "style": "primary",
          "color": "#009100"
        }
      ],
      "spacing": "sm"
    },
    "styles": {
      "header": {
        "backgroundColor": "#345328"
      }
    }
  }
  return result

def cardCourse( className, classID, teacherName, score ) :
  card = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://inside-assets1.inside.com.tw/2015/08/giphy.gif.pagespeed.ce_.592JmPrI7u.gif?auto=compress&fit=max&w=705",
    "size": "full",
    "aspectRatio": "20:13",
    "action": {
      "type": "uri",
      "uri": "https://www.youtube.com/watch?v=xvFZjo5PgG0&ab_channel=Duran"
    },
    "margin": "none",
    "aspectMode": "cover",
    "animated": True
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": className,
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "課程代碼",
                "color": "#000000",
                "size": "sm",
                "wrap": True,
                "decoration": "none"
              },
              {
                "type": "text",
                "text": classID,
                "wrap": True,
                "color": "#000000",
                "size": "sm",
                "align": "end"
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "老師名稱",
                "color": "#000000",
                "size": "sm",
                "wrap": True
              },
              {
                "type": "text",
                "text": teacherName,
                "wrap": True,
                "color": "#000000",
                "size": "sm",
                "align": "end"
              }
            ]
          }
        ]
      },
      {
        "type": "box",
        "layout": "horizontal",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "推薦指數",
            "color": "#000000",
            "size": "sm"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": score + "%",
                "backgroundColor": "#C98CA7",
                "margin": "none",
                "height": "15px"
              }
            ],
            "backgroundColor": "#E5D1D0",
            "margin": "sm",
            "spacing": "none",
            "height": "15px"
          },
          {
            "type": "text",
            "text": score,
            "size": "sm",
            "color": "#5B5B5B",
            "margin": "md",
            "flex": 0
          }
        ]
      }
    ],
    "backgroundColor": "#ADB6C4"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "看文字評價",
          "text": classID + className
        },
        "color": "#001B2E"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "margin": "sm"
      }
    ],
    "flex": 0,
    "backgroundColor": "#ADB6C4"
  }
}
  return card

def textCommentCard( className, classID, teacherName, textComment ) :
  textCommentCard = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://i.giphy.com/media/pOZhmE42D1WrCWATLK/giphy.webp",
    "size": "full",
    "aspectRatio": "20:13",
    "action": {
      "type": "uri",
      "uri": "https://www.youtube.com/watch?v=xvFZjo5PgG0&ab_channel=Duran"
    },
    "margin": "none",
    "aspectMode": "cover",
    "animated": True
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": className,
            "align": "start",
            "wrap": True,
            "size": "xl",
            "color": "#000000",
            "weight": "bold"
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": textComment,
            "size": "lg",
            "wrap": True
          }
        ]
      }
    ],
    "backgroundColor": "#C9B1BD"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "text",
            "text": "課程代碼",
            "size": "sm",
            "align": "start",
            "wrap": True
          },
          {
            "type": "text",
            "text": classID,
            "align": "end",
            "wrap": True,
            "size": "sm"
          }
        ]
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "text",
            "text": "老師名字",
            "align": "start",
            "wrap": True,
            "size": "sm"
          },
          {
            "type": "text",
            "text": teacherName,
            "align": "end",
            "wrap": True,
            "size": "sm"
          }
        ]
      }
    ],
    "backgroundColor": "#D5DFE5"
  }
}
  return textCommentCard

def carousel( bubble ) :
  Carousel_Class =    {
  "type": "carousel",
  "contents": bubble
}
  return Carousel_Class

def chooseTeacher( button ) :
  teacher = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "選擇教授",
        "weight": "bold",
        "size": "xl",
        "wrap": True,
        "color": "#FFFFFF"
      }
    ],
    "backgroundColor": "#5FB49C"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": button,
    "flex": 0,
    "backgroundColor": "#DEEFB7"
  }
}
  return teacher

def teacherButton( teacherName ) :
  button =   {
  "type": "button",
  "action": {
  "type": "message",
  "label": teacherName,
  "text": teacherName
  },
  "color": "#98DFAF",
  "style": "secondary",
  "height": "sm"
}
  return button

def card(restaurant_name,restaurant_image,restaurant_address,restaurant_rate,restaurant_distance): #三家餐廳用
  output = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": restaurant_image,
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": restaurant_name,
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "評分",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": restaurant_rate,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "距離",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": restaurant_distance,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "Google地圖",
          "uri": "https://www.google.com/maps/place/" + restaurant_address
        }
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "margin": "sm"
      }
    ],
    "flex": 0
  }
}

  return output

def carousel_restaurant(bubble): #三家餐廳用
  output = {
  "type": "carousel",
  "contents": bubble
    
}
  return output

def card2(menu,text): #菜單用
  
  output = {
    "type": "bubble",
    # "hero": {
    #   "type": "image",
    #   "url": "https://prospective-students.cycu.edu.tw/wp-content/uploads/2018/11/home_about_bg-1.jpg",
    #   "size": "full",
    #   "aspectRatio": "20:13",
    #   "aspectMode": "cover",
    #   "action": {
    #     "type": "uri",
    #     "uri": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    #   }
    # },
    "body": {
      "type": "box",
      "layout": "vertical",
      "spacing": "md",
      "action": {
        "type": "uri",
        "uri": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
      },
      "contents": [
        {
          "type": "text",
          "text": text,
          "size": "xl",
          "weight": "bold"
        },
        {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": 
            menu
          
        }
      ]
    }
  }

  return output

def card2_time_content(day,time):
  output = {
              "type": "box",
              "layout": "baseline",
              "contents": [
                
                {
                  "type": "text",
                  "text": day,
                  "weight": 'bold',
                  "margin": 'sm',
                  "flex": 0
                  
                },
                {
                  "type": "text",
                  "text": time,
                  "size": "sm",
                  "align": "end",
                  "color": "#aaaaaa"
                }
              ]
            }
  return output

def card2_menu_content(name,num,pirce):
  if name == '':
    name = ' '
  elif len(name) > 20 :
    name = name[0:20]
  if pirce == '':
    pirce = ' '
  elif len(pirce) > 20 :
    pirce = pirce[0:20]

  if (num%3) == 0:
    word = 'xs'
    word2 = 'regular'
    color = '#9D9D9D'
  else:
    word = 'sm'
    word2 = 'bold'
    color = '#000000'

  output = {
              "type": "box",
              "layout": "baseline",
              "contents": [

                {
                  "type": "text",
                  "text": name,
                  "weight": word2,
                  "margin": word,
                  "flex": 0,
                  "color": color
                },
                {
                  "type": "text",
                  "text": pirce,
                  "size": "sm",
                  "align": "end",
                  "color": "#aaaaaa"
                }
              ]
            }
  return output
def book_list(course,book_name):
  result={
    "type": "bubble",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": course,
          "color": "#FFFFFF",
          "size": "3xl"
        }
      ]
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": 
        book_name
      ,
      "spacing": "sm"
    },
    "styles": {
      "header": {
        "backgroundColor": "#251605"
      }
    }
  }
  return result

def book_name_list(book_name):
  result = {
    "type": "button",
    "action": {
      "type": "message",
      "label": book_name[:40],
      "text": book_name
    },
    "style": "primary",
    "color": "#E2C391",
    "wrap": True
  }
  return result

def endCommentResult( listOfScore, className,str_List ) :
  result = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://i.giphy.com/media/26ufp2LYURTvL5PRS/giphy.webp",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "https://www.youtube.com/watch?app=desktop&v=xvFZjo5PgG0&ab_channel=Duran"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": className,
        "weight": "bold",
        "size": "xxl"
      },
      {
        "type": "text",
        "text": "作業量好評",
        "size": "md"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "width": str( listOfScore[0] ) + "%",
                "backgroundColor": "#D1B1C8",
                "height": "6px"
              }
            ],
            "backgroundColor": "#8C7284",
            "height": "6px",
            "margin": "sm"
          },
          {
            "type": "text",
            "text": str_List[0],
            "margin": "none",
            "flex": 0,
            "wrap": True,
            "color": "#6C6C6C"
          }
        ]
      },
      {
        "type": "text",
        "text": "課程難易度好評",
        "size": "md"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "width": str( listOfScore[1] ) + "%",
                "backgroundColor": "#D1B1C8",
                "height": "6px"
              }
            ],
            "backgroundColor": "#8C7284",
            "height": "6px",
            "margin": "sm"
          },
          {
            "type": "text",
            "text": str_List[1],
            "margin": "none",
            "flex": 0,
            "wrap": True,
            "color": "#6C6C6C"
          }
        ]
      },
      {
        "type": "text",
        "text": "學到東西多寡好評",
        "size": "md"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "width": str( listOfScore[2] ) + "%",
                "backgroundColor": "#D1B1C8",
                "height": "6px"
              }
            ],
            "backgroundColor": "#8C7284",
            "height": "6px",
            "margin": "sm"
          },
          {
            "type": "text",
            "text": str_List[2],
            "margin": "none",
            "flex": 0,
            "wrap": True,
            "color": "#6C6C6C"
          }
        ]
      },
      {
        "type": "text",
        "text": "給分甜不甜好評",
        "size": "md"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "width": str( listOfScore[3] ) + "%",
                "backgroundColor": "#D1B1C8",
                "height": "6px"
              }
            ],
            "backgroundColor": "#8C7284",
            "height": "6px",
            "margin": "sm"
          },
          {
            "type": "text",
            "text": str_List[3],
            "margin": "none",
            "flex": 0,
            "wrap": True,
            "color": "#6C6C6C"
          }
        ]
      }
    ],
    "backgroundColor": "#B1B7D1"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "此為這堂課所有蒐集到的評價結果統計。",
        "size": "sm",
        "margin": "none"
      }
    ],
    "backgroundColor": "#9B9FB5"
  }
  }
  return result