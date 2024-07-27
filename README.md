# Video-Compress-Release
A Simple Video Compress Tool

# 文档更新日期2024/2/4

# 文件目录树
    -temp //程序临时处理文件夹 请不要自行创建或在temp中存放文件
    -compress.exe // 视频处理主程序
    -subinfo.exe //查看mkv字幕轨信息
    -core.exe // 视频编码程序不需要打开  **ffmpeg的编译程序 请自行改名 或者修改源码**
    -config.json // 程序配置文件
    -output // 视频输出文件夹

# 配置解析
    程序第一次启动时会要求输出key和mode并保存在config.json中，后续需要修改请打开config.json文件修改，或者直接删除config.json程序会引导重新进行配置
    config.json程序配置中包含变量mode

    关于mode的设置有以下十个选择，压制速度从快到慢，效果从差到好。如果不知道怎么取舍请默认输入medium，程序将以较为平衡的方式进行处理
    ultrafast
    superfast
    veryfast
    faster
    fast
    medium
    slow
    slower
    veryslow
    placebo

# 程序功能
	1.MP4到MP4 //对MP4进行二次压制
	2.MKV压制内封字幕到MP4 //将MKV内封字幕与视频进行压制为MP4
	两种模式都可以对文件夹内所有视频进行批量处理
	MKV选择压制字幕轨道索引时 可以使用subinfo.exe查看MKV内封字幕轨道的信息
   是否压制水印(y/n)
   	输入y压制 n不压制

# 处理速度判断
    在视频处理时，输出日志的最末尾会有如 2.00x 的字样
    则当前处理速度为两倍速，那么一个24分钟的视频处理时间约为24/2=12分钟
