# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 20:53:54 2017

@author: Administrator
"""
import cv2
import csv
import numpy as np
from skimage import io
import time

height=421#y
width=548#x
city0=(142,328)
citys=((84,203),(199,371),(140,234),(236,241),(315,281),(358,207),(363,237),(423,266),(125,375),(189,274))


def city_location():
      #读取城市坐标，显示
      city_reader = csv.reader(open('CityData.csv', 'r'))
      image=cv2.imread('void.png')
      for row in (city_reader):
            if row[0]=='cid':
                  continue
            #print(row)
            x=int(row[1])
            y=int(row[2])
            cv2.circle(image,(x,y),5,(200,20,20),-1)#修改最后一个参数
            
      cv2.imwrite("city_location.png",image)
      print ("读取城市坐标成功")


def In_situ():
    #读取天气预测
    image=cv2.imread('void.png')
    In_situMeasurementforTraining = csv.reader(open('In-situMeasurementforTraining_20171124.csv', 'r'))
    #['xid', 'yid', 'date_id', 'hour', 'wind']
    for row in (In_situMeasurementforTraining):
        if row[0]=='xid':
            continue
        x=int(row[0])
        y=int(row[1])
        data=int(row[2])
        hour=int(row[3])
        wind=int(float(row[4]))*10
        if wind>250:
            wind=250
        if wind<150:
            wind=0
        image[y,x,0]=wind
        image[y,x,1]=wind
        image[y,x,2]=wind

        #print(width,x,height,y)
        if x==width and y==height:
            number="In_situ/3/"+"D"+str(data)+"H"+str(hour)+".png"
            print(number)
            cv2.circle(image,city0,1,(255,255,255),-1)#起点
            for i in range(10):
                cv2.circle(image,citys[i],1,(255,100+i*10,100-i*10),-1)#终点
            cv2.imwrite(number,image)
            for x in range(width):
                for y in range(height):
                    image[y,x,0]=0
                    image[y,x,1]=0
                    image[y,x,2]=0
      #prin ("读取天气真值信息成功")
      
def Forecastdata():
    #获取天气预测数据-training   ForecastDataforTesting_20171124
    #['xid', 'yid', 'date_id', 'hour', 'model', 'wind']
    #ForecastData = csv.reader(open('ForecastDataforTraining_20171124.csv', 'r'))
    ForecastData = csv.reader(open('ForecastDataforTesting_20171124.csv', 'r'))
    img=[]
    for i in range(10):
        img.append(cv2.imread('void.png'))
    
    for row in  ForecastData:
          if row[0]=='xid':
                continue
          x=int(row[0])
          y=int(row[1])
          data=int(row[2])
          hour=int(row[3])
          model=int(row[4])
          wind=int(float(row[5]))*10
          if wind>=250:
              wind=250
          if wind<150:
              wind=0
          img[model-1][y,x,0]=wind
          img[model-1][y,x,1]=wind
          img[model-1][y,x,2]=wind
          if x== width and y==height and model==10:
              for i in range(10):
                  #number="ForecastTrain/"+str(i+1)+"/"+"D"+str(data)+"H"+str(hour)+"M"+str(i+1)+".png"
                  number="ForecastTest2/"+str(i+1)+"/"+"D"+str(data)+"H"+str(hour)+"M"+str(i+1)+".png"
                  print(number)
                  cv2.imwrite(number,img[i])
              for k in range(10):
                  for x in range(width):
                      for y in range(height):
                          img[k][y,x,0]=0
                          img[k][y,x,1]=0
                          img[k][y,x,2]=0


def A_star_withtime(day,informap,city0,citynum):
    minroad=[]#存储最佳路径
    lenminroad=10000#记录最佳路径长度
    
    pic=[]#读取当天所有时刻地图
    for i in range(3,21):
        nameofpic="In_situ/2/"+"D"+str(day)+"H"+str(i)+".png"#读取不同时刻的图片
        pic.append(cv2.imread(nameofpic,cv2.IMREAD_GRAYSCALE))  

    dj=abs(citys[citynum][0]-city0[0])+abs(citys[citynum][1]-city0[1])#L型路径代价
    star={'位置':city0,'代价':dj,'父节点':city0,'索引':[0,0],'风速':0,'时刻':3}#起点
    end={'位置':citys[citynum],'代价':dj,'父节点':citys[citynum],'索引':[10000,10000],'风速':0,'时刻':21}#终点
    openlist=[]#open列表，存储可能路径
    closelist=[star]#close列表，已走过路径
    index=0#节点在closelist路径中的索引
    hourlast=0#方便打印当前时刻
    
    hour=0
    step=0
    while(1):
        step+=1
        x=star['位置'][0]
        y=star['位置'][1]
        if pic[int(step/30)][y,x]>150:
            index+=1
            pointadd={'位置':city0,'代价':dj,'父节点':city0,'索引':[index,index-1],'风速':150,'时刻':int((step+1)/30)}#起点
            closelist.append(pointadd)
        else:
            break
    #print(closelist)
    
    
    while(1):  
        #追溯当前路径步数
        step=1#当前追溯路径的步数
        point=closelist[-1] 
        while 1:            
            sy=point['索引'][1]
            point=closelist[sy]
            step+=1
            if point==star:
                #print("共走过步数:",step)
                break
            
        #四个方向搜索可能路径
        s_point=closelist[-1]#获取close列表最后一个点位置，S点
        add=([0,0],[0,1],[0,-1],[1,0],[-1,0])#可能运动的四个方向增量
        for i in range(len(add)):
            x=s_point['位置'][0]+add[i][0]
            y=s_point['位置'][1]+add[i][1]
            hour=int(step/30)+3#每30步一小时
            if hour>=21:#超过当天最迟时刻
                print('超过当天最迟时刻')
                break
            windpic=pic[hour-3]#根据追溯路径确定当前时刻的地图
            if x<0 or x>=width or y<0 or y>=height or windpic[y,x]>=150:
                continue                #超过地图边界和风速大于150，跳过
            
            #计算代价
            G=abs(x-star['位置'][0])+abs(y-star['位置'][1])#计算代价
            H=abs(x-end['位置'][0])+abs(y-end['位置'][1])#计算代价
            T=0
            barrier_range=10#搜索障碍物范围
            for i in range(barrier_range):
                if x-i<=0 or x+i>=width or y-i<=0 or y+i>=height:
                    T=(barrier_range-i)
                    break
                if windpic[y,x+i]>150:
                    informap[y,x+i,0]=windpic[y,x+i]
                    informap[y,x+i,1]=windpic[y,x+i]
                    informap[y,x+i,2]=windpic[y,x+i]
                    T=(barrier_range-i)
                    break
                if windpic[y+i,x]>150:
                    informap[y+i,x,0]=windpic[y+i,x]
                    informap[y+i,x,1]=windpic[y+i,x]
                    informap[y+i,x,2]=windpic[y+i,x]
                    T=(barrier_range-i)
                    break
                if windpic[y,x-i]>150:
                    informap[y,x-i,0]=windpic[y,x-i]
                    informap[y,x-i,1]=windpic[y,x-i]
                    informap[y,x-i,2]=windpic[y,x-i]
                    T=(barrier_range-i)
                    break
                if windpic[y-i,x]>150:
                    informap[y-i,x,0]=windpic[y-i,x]
                    informap[y-i,x,1]=windpic[y-i,x]
                    informap[y-i,x,2]=windpic[y-i,x]
                    T=(barrier_range-i)
                    break
            T=float(H)/float(G+H)*float(T)*(5.0+T)
            F=G+H+T
            
            #判断新增点是否可以加入到两个列表中
            count=0
            for i in openlist:
                if i['位置']==(x,y) and i['代价']==F:#考虑到障碍物位置到变化，代价不同说明是不同时刻
                    count+=1
            for i in closelist:
                if i['位置']==(x,y) and i['代价']==F:
                    count+=1
            if count==0:#新增点不在open和close列表中
                fatherlocation=s_point['位置']
                indexfather=s_point['索引'][0]
                addpoint={'位置':(x,y),'代价':F,'父节点' :fatherlocation,'索引':[0,indexfather],'风速':windpic[y,x],'时刻':hour}#更新位置
                #索引0为自身节点，1为父节点
                openlist.append(addpoint)
                
            
        t_point={'位置':(50,50),'代价':10000,'父节点':(50,50),'索引':[0,0],'风速':0,'时刻':3}
        for j in range(len(openlist)):#寻找代价最小点
            if openlist[j]['代价']<t_point['代价']:
                t_point=openlist[j]
        for j in range(len(openlist)):#在open列表中删除t点
            if t_point==openlist[j]:
                openlist.pop(j)
                break
        
        index+=1#索引加1，最开始索引0为star
        t_point['索引'][0]=index
        closelist.append(t_point)#在close列表中加入t点
        cv2.circle(informap,t_point['位置'],1,(200,255,255),-1)
        #cv2.circle(windpic,t_point['位置'],1,200,-1)
        
        if hourlast!=hour:
            hourlast=hour
            print("day",day,"city:",citynum,"hour",hour,"step",step)
            if hour>=21:
                print('超过当天最迟时刻')
                break
        if t_point['位置']==end['位置']:#找到终点！！
            print("找到终点!!",'day:',day,'city:',citynum)
            break
        if step>=630:
            print("已经走630步了，还没找到。根据需要设一个阈值，搜索太久可能是没有可行路径了，建议这个值为dj的倍数")
            break
    
    #print(closelist)
    #逆向搜索找到路径
    road=[]        
    point=closelist[-1] 
    while 1:      
        road.append(point)
        sy=point['索引'][1]
        point=closelist[sy]
        if point==star:
            print("路径搜索完成")
            break
        
    #print(road)
    
    if len(road)<lenminroad:
        minroad=road
        minstep=step
        lenminroad=len(minroad)
    print('最终minstep is :',minstep,lenminroad)
    
    for i in minroad:#画出规划路径
        x=i['位置'][0]
        y=i['位置'][1]
        informap[y,x,0]=200
        informap[y,x,1]=i['时刻']*10
        informap[y,x,2]=i['时刻']*10
        windpic[y,x]=i['时刻']*10
        
    cv2.circle(informap,star['位置'],1,(0,255,0),-1)#起点
    cv2.circle(informap,end['位置'],1,(0,255,100),-1)#终点
    #io.imshow(informap)
    cv2.imwrite("road/"+str(day)+str(citynum+1)+"informap.png",informap)
    cv2.circle(windpic,star['位置'],1,255,-1)#起点
    cv2.circle(windpic,end['位置'],1,255,-1)#终点
    cv2.imwrite("road/"+str(day)+str(citynum+1)+"informapshow.png",windpic)
    
    return minroad


def writeroad2csv(citynum,day,road): 
    with open("road.csv","a+") as csvfile: 
        writer = csv.writer(csvfile)
        road=road[::-1]
        for i in road:
            writer.writerow([citynum,day,i['时刻'],i['位置'][0],i['位置'][1]])



          
