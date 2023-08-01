#根据预定的csv数据自动回复
import numpy as np
import pandas as pd
from uiautomation import WindowControl
import time
wx = WindowControl(Name='微信', searchDepth=1)   #searchDepth=1参数指定在查找窗口时只搜索直接子级窗口，以提高查找效率
wx.ListControl()
wx.SwitchToThisWindow()#ListControl()方法用于列出所有子级窗口，而SwitchToThisWindow()方法则将焦点切换到微信主窗口
hw = wx.ListControl(Name='会话')
df = pd.read_csv('回复数据.csv', encoding='utf-8')
print(df)
# 死循环接收消息
while True:
    we = hw.TextControl(searchDepth=4)
    while not we.Exists():
        pass
    if we.Name:
        we.Click(simulateMove=False)
        message_list = wx.ListControl(Name='消息').GetChildren()#获取消息列表中的所有子控件
        last_msg = message_list[-1].Name
        # 判断关键字
        msg = df.apply(lambda x: x['回复内容'] if x['关键词'] in last_msg else None, axis=1)
        print(f"匹配到的回复内容：{msg}")
        # 数据筛选，移除空数据
        msg.dropna(axis=0, how='any', inplace=True)
        # 做成列表
        ar = np.array(msg).tolist()
        # 能够匹配到数据时
        if ar:
            # 将数据输入并替换换行符号
            wx.SendKeys(ar[0].replace('{br}', '{Shift}{Enter}'), waitTime=0)
            # 发送消息，回车键
            wx.SendKeys('{Enter}', waitTime=0)
        else:
            wx.SendKeys('不知道你在说什么', waitTime=0)
            wx.SendKeys('{Enter}', waitTime=0)
            wx.SendKeys('{Enter}', waitTime=0)
    # 添加适当的延时等待
    #time.sleep(1)