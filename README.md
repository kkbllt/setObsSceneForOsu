#注意事项

###此工具依赖于下列项目，请确保已经知悉对应项目的是用
osb https://github.com/obsproject/obs-studio  
Gosumemory https://github.com/l3lackShark/gosumemory  
LLin https://github.com/MATRIX-feather/LLin/  
python  

   
##使用方法
####工具端
>git clone https://github.com/kkbllt/setObsSceneForOsu.git  
>cd setObsSceneForOsu  
>>pip install -r requirements.txt  
>>or  
>>pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple  

>python getGosuMemory.py

####obs端
>工具->脚本  
>1. python设置->填入你的python安装目录(加载成功会显示你的python版本)  
>2. 脚本  
>>添加脚本  
>>找到工具端的目录  
>>加载文件名为“obsSetSense.py”的脚本  
>>根据说明提示选择obs场景  