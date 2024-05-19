# 注意事项

### 此工具依赖于下列项目，请确保已经知悉对应项目的使用
osb https://github.com/obsproject/obs-studio  
tosu https://github.com/KotRikD/tosu  
LLin https://github.com/MATRIX-feather/LLin/  
python  ver3.9

   
## 使用方法  
#### 工具端  
>git clone https://github.com/kkbllt/setObsSceneForOsu.git  
>cd setObsSceneForOsu  
>pip install -r requirements.txt  
>python getGosuMemory.py  
>  
>如网络较差可以在pip指令最后添加 -i https://pypi.tuna.tsinghua.edu.cn/simple 来临时使用tuna源加速  
>为确保资源实时性请勿添加任何timesleep
  
  
#### obs端
>工具->脚本  
>1. python设置->填入你的python安装目录(加载成功会显示你的python版本)  
>2. 脚本  
>>添加脚本  
>>找到工具端的目录  
>>加载文件名为“obsSetSense.py”的脚本  
>>根据说明提示选择obs场景  
  
  
#### 一些值的解析
>osbuSetSense  
>>res \[_play_state', 'mapdatastr', 'allGosumemoryData'\]  
>>res\[0\] '_play_state' int 返回你的游戏状态  
>>res\[1\] 'mapdatastr' str 经过getGosuMemory处理的简易文本  
>>res\[2\] 'allGosumemoryData' str tosu/LLin返回的原始数据  
>
>app(url) 可选参数url如果你的GosuMemory有修改过ws服务器地址则需要填写。示例app(url = 'ws//127.0.0.1:24050/ws')
