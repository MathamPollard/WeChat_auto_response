#根据预定的csv数据自动回复
import numpy as np
import pandas as pd
from uiautomation import WindowControl
import time
import requests
# 绑定微信主窗口
wx = WindowControl(Name='微信', searchDepth=1)   #searchDepth=1参数指定在查找窗口时只搜索直接子级窗口，以提高查找效率
# 切换窗口
wx.ListControl()
wx.SwitchToThisWindow()#ListControl()方法用于列出所有子级窗口，而SwitchToThisWindow()方法则将焦点切换到微信主窗口
# 寻找会话控件绑定
hw = wx.ListControl(Name='会话')
# 通过pd读取数据
df = pd.read_csv('回复数据.csv', encoding='utf-8')
print(df)

conversations = hw.GetChildren()  # GetChildren()方法，获取会话列表中的所有子控件。
jilu_num = 0
for conversation in conversations:
    contact_name = conversation.Name
    if contact_name == '水果巨亨':   #改成你想回复的联系人的名字
        conversation.Click(simulateMove=False)
        message_list = wx.ListControl(Name='消息').GetChildren()  # 获取消息列表中的所有子控件
        jilu_num = len(message_list)
        print(f"原本有{jilu_num}条消息")
# 死循环接收消息
while True:
    for conversation in conversations:
        contact_name = conversation.Name
        if contact_name == '水果巨亨':
            #conversation.Click(simulateMove=False)
            message_list = wx.ListControl(Name='消息').GetChildren()  # 获取消息列表中的所有子控件
            new_msg_num = len(message_list)-jilu_num
            if new_msg_num != 0:
                print(f"有{new_msg_num}条新消息：")
                for i in range(jilu_num, len(message_list)):
                    print(f"正在回复第{i+1}条消息")
                    #处理每一条消息
                    every_msg = message_list[i].Name
                    ##########
                    # 判断关键字
                    msg = df.apply(lambda x: x['回复内容'] if x['关键词'] in every_msg else None, axis=1)
                    # 返回的结果是一个包含处理结果的Series对象，msg和列表差不多
                    print(f"匹配到的回复内容：{msg}")
                    msg.dropna(axis=0, how='any', inplace=True)  # 这行代码移除回复内容中的空数据（NaN值）
                    ar = np.array(msg).tolist()  # 这行代码将筛选后的回复内容转换为列表
                    # 能够匹配到数据时
                    if ar:
                        # 将数据输入
                        # 替换换行符号
                        wx.SendKeys(ar[0].replace('{br}', '{Shift}{Enter}'), waitTime=0)
                        # 发送消息，回车键
                        wx.SendKeys('{Enter}', waitTime=1)
                        # 通过消息匹配检索会话栏的联系人
                        print(f"回复内容是 {ar[0]}")
                        #wx.TextControl(SubName=ar[0][:5]).RightClick()
                        # break
                    #########不能匹配到数据，用机器人回复
                    else:
                        wx.SendKeys('不知道你在说什么', waitTime=0)
                        wx.SendKeys('{Enter}', waitTime=0)
                jilu_num = len(message_list) + 1
                print(f"现在一共有{jilu_num}条消息")
            else:
                print("没有新消息")