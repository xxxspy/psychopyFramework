#encoding:utf8
#!/usr/bin/env python2


from psychopy import data,visual,event,core,gui
import time
import math


#配置变量##############################################
extraInfo= {'name':'input your name','participantID':1,'session':1,'gender':['male','female'],'age':20,'hand':['left','right']}
paraList=['score','fscore1','fscore2','fscore3','isgenerous','cut']#需要记录的指标

#####结束配置变量######################################

dlg=gui.DlgFromDict(dictionary=extraInfo,title='this is title')




######刺激对象#############################################


#c创建一个windows用于呈现刺激，所有的刺激对象都需要windows来呈现
win = visual.Window(fullscr=False,size=(1224,798),  monitor='testMonitor',allowGUI=True, color=(-1,-1,-1), units='cm')
#设置windows的位置位于屏幕中央
win.viewPos=(0,0)

#指导语text，如果指导语很简单可以用它
instructionText=visual.TextStim(win, pos=[0,0.0])
tsim=visual.TextStim(win, pos=[0,0.0])
#tipText=visual.TextBox(win,pos=[0,-1],text=u'\u63d0\u793a\u8bed' ,font_size=20,size=(0.5,0.3),font_color=[-1,1,1],align_horz='center')



#以上创建的对象都还没有绘制到屏幕上
#只是先创建好，放在这里，以后备用

def draw(*args):
    '''绘制到屏幕上'''
    for i in args:
        i.draw()

###############Classes#######################
#这里放置一些类

#######################################################
def wait(maxWait=60*60,keyList=[]):
    if 'esc' not in keyList:keyList.append('esc')
    if 'escape' not in keyList:keyList.append('escape')
    keys = event.waitKeys(maxWait=maxWait,keyList=keyList,timeStamped=False)#等待按键
    timestamp=getTimeStamp()
    keys= keys if keys else [None]
    if keys[0] in ['esc','escape']:core.quit()
    return keys[0],timestamp


def getTimeStamp():
    '''获取时间戳'''
    return time.time()

def gener_trialhandler(filename, selection=':',paraList=[]):
    '''
    生成试次列表
    ------------
    selection: 切片
    filename: 保存试次信息的excel文件
    paraList: 需要记录的参数名称
    '''
    trials = data.TrialHandler(nReps=1.0,method='random', 
                                extraInfo=extraInfo,originPath=None,
                                trialList=data.importConditions(filename,selection=selection),
                                name='trials')
    for p in paraList:
        trials.data.addDataType(p)
    return trials


def draw_instructions(texts=[], pics=[]):
    '''即可用文字指导语，又可以用图片指导语，但是不能同时用两种
    建议用图片，可以控制格式，因为psychopy对中文支持不友好'''
    if texts:
        for i in texts:
            i.draw()
            win.flip()
            wait(keyList=['space'])
    elif pics:
        instructionImg= visual.ImageStim(win, pos=(0,0), units='deg')
        for i in  pics:
            instructionImg.image=i 
            instructionImg.draw()
            win.flip()
            wait(keyList=['space'])


def gener_blocks():
    '''创建所有的trails'''
    trails=gener_trialhandler(filename='conditions/cons1.xlsx' , paraList=['new_parameter'])
    blocks=[trails, ]#list of lists
    return blocks


    

def showblock(block, text_instructions=[],pic_instructions=[]):
    draw_instructions(pics=pic_instructions, texts=text_instructions)
    for trial in block:
        #这里开始呈现刺激
        # draw someting
        tsim.text=trial['alpha']
        tsim.draw()
        win.flip()
        key, timestamp=wait(keyList=['f','j'])
        block.addData('pressedKey', key)
        block.addData('pressedTime', timestamp)




def experiment():
    #显示指导语，按空格键翻页
    draw_instructions(pics=['pics/instructions/instruction0.bmp',])
    blocks=gener_blocks()
    num=0
    for block in blocks:
        num +=1
        showblock(block, pic_instructions=['pics/instructions/instruction1.bmp'])
        block.saveAsExcel('datas/%s_%s_data.xlsx' % ( str(extraInfo['participantID']),str(extraInfo['session'])),dataOut=("all_raw",))
        


if __name__=='__main__':
    experiment()
    print ('finished')
    
                    
       