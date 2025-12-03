import math
from softwareEvaluation import soft_evaluation
from random import randint
import time
token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
eyJleHAiOjE2Njk5MDA1MDUsInVzZXJuYW1lIjoi5byg\
5LiJIn0.Q6YFZVEte9syYnUNv_drVDyqvZdyCQ7iRAKwj_\
kYxYI2ac44369-d85d-4716-a33a-71e49831660c'
type_name="22720_化工设备梯子平台绘图软件"
operate_type=['绘制塔平台立面图',
              '绘制塔平台平面图',
              '绘制支耳一览表',
              '绘制预焊件一览表',
              '绘制材料表',
              '绘制塔外壁展开图',
              '绘制卧式平台立面图',
              '绘制卧式平台平面图',
              '绘制卧式平台左视图',]
for i in range(randint(10,20)):
    time.sleep(randint(1,10))
    print(soft_evaluation.soft_evaluation\
          (token,type_name,operate_type[randint(0,8)]))
