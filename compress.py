import subprocess
import os
import sys
import uuid
import requests
import hashlib
import json
import time
import base64


# 视频压制函数
def mp4compress(input_video, mode, output_video, islogo):
    if os.path.exists("temp"):
        pass
    else:
        os.mkdir("temp")
    if islogo == "n":
        # 不压制水印代码
        command = f'core.exe -i {input_video} -metadata comment="Powered By XXX" -c:v libx264 -crf 25 -preset {mode} -pix_fmt yuv420p -vf "hqdn3d=0.5:0.5:0.5:0.5,deband,unsharp=luma_amount=0.5" -hide_banner -y {output_video}'
    else:
        creatlogo()
        # 压制水印代码
        command = f'core.exe -i {input_video} -i temp//temp.png -filter_complex "[1:v]scale=-1:iw/15[watermark];[0:v][watermark]overlay=20:20[v]" -map "[v]" -map 0:a -c:v libx264 -crf 25 -preset {mode} -pix_fmt yuv420p -metadata comment="Powered By XXX" -hide_banner -y {output_video}'
    subprocess.call(command, shell=True)
    try:
        os.remove("temp\\temp.png")
    except:
        pass
    os.rmdir("temp")


def mkvcompress(input_video, sub_index, mode, output_video, islogo):
    if os.path.exists("temp"):
        pass
    else:
        os.mkdir("temp")
    # 先提取视频
    mkvtomp4 = (
        f"core.exe -i {input_video} -c:v copy -c:a copy -hide_banner -y temp//temp.mp4"
    )
    subprocess.call(mkvtomp4, shell=True)
    # 再提取字幕
    mkvtoass = f"core.exe -i {input_video}  -map 0:s:{sub_index} -hide_banner -y temp//temp.ass"
    subprocess.call(mkvtoass, shell=True)
    # 将字幕烧录进视频
    if islogo == "n":
        # 不压制水印代码
        assinmp4 = f'core.exe -i temp//temp.mp4 -metadata comment="Powered By XXX" -c:v libx264 -crf 25 -preset {mode} -pix_fmt yuv420p -vf "ass=temp//temp.ass,hqdn3d=0.5:0.5:0.5:0.5,deband,unsharp=luma_amount=0.5" -hide_banner -y {output_video}'
    else:
        creatlogo()
        # 压制水印代码
        assinmp4 = f'core.exe -i temp//temp.mp4 -i temp//temp.png -filter_complex "[0:v]subtitles=temp//temp.ass[v];[1:v]scale=-1:iw/15[watermark];[v]hqdn3d=0.5:0.5:0.5:0.5,deband,unsharp=luma_amount=0.5[vf];[vf][watermark]overlay=20:20[outv]" -map "[outv]" -map 0:a -c:v libx264 -crf 25 -preset {mode} -pix_fmt yuv420p -metadata comment="Powered By XXX" -hide_banner -y {output_video}'
    subprocess.call(assinmp4, shell=True)
    try:
        os.remove("temp\\temp.png")
    except:
        pass
    os.remove("temp\\temp.mp4")
    os.remove("temp\\temp.ass")
    os.rmdir("temp")


# 设备授权校验
# def authorization(key):
#     try:
#         callback = requests.get(
#             "https://www.example.top/authentication/deviceCheck.php?deviceID="
#             + str(uuid.getnode())
#         ).json()
#         if (
#             callback["data"]
#             == hashlib.md5(
#                 (
#                     hashlib.md5(str(uuid.getnode()).encode()).hexdigest()
#                     + str(callback["time"])
#                     + key
#                 ).encode()
#             ).hexdigest()
#         ):
#             return True
#         else:
#             return False
#     except:
#         return False


# 水印生成函数
def creatlogo():
    base64_string = "data:image/png;base64,XXXXXXX"
    # 移除base64字符串中的前缀 'data:image/png;base64,'
    base64_string = base64_string.replace("data:image/png;base64,", "")
    # 解码base64字符串
    image_data = base64.b64decode(base64_string)
    # 将图像数据保存为图片文件
    with open("temp//temp.png", "wb") as f:
        f.write(image_data)


# 切换工作目录
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

# 读取配置文件
print("==================================================")
print("开始载入配置文件...")
print("当前时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print("==================================================")
if (
    os.path.exists(os.path.join(os.path.abspath("."), "config.json"))
    and os.path.getsize(os.path.join(os.path.abspath("."), "config.json")) > 0
):
    # 如果文件存在，读取其中的值
    with open(os.path.join(os.path.abspath("."), "config.json"), "r") as f:
        config = json.load(f)
        # # 判断是否存在key和mode，如果有就取出值
        # if "key" in config:
        #     key = config["key"]
        # else:
        #     # 如果没有，从用户输入中获取
        #     key = input("请输入KEY:")
        #     # 更新config字典
        #     config["key"] = key
        #     # 将config字典写入json文件中
        #     with open(os.path.join(os.path.abspath("."), "config.json"), "w") as f:
        #         json.dump(config, f)
        if "mode" in config:
            mode = config["mode"]
        else:
            # 如果没有，从用户输入中获取
            mode = input("请输入MODE:")
            # 更新config字典
            config["mode"] = mode
            # 将config字典写入json文件中
            with open(os.path.join(os.path.abspath("."), "config.json"), "w") as f:
                json.dump(config, f)
else:
    # 如果文件不存在，获取用户输入
    # key = input("请输入KEY:")
    mode = input("请输入MODE:")
    # 将键值对存入字典中
    # config = {"key": key, "mode": mode}
    config = {"mode": mode}
    # 将字典写入json文件中
    with open(os.path.join(os.path.abspath("."), "config.json"), "w") as f:
        json.dump(config, f)

print("配置处理完毕")
print("==================================================")
print("当前时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print("开始进行鉴权...")

# 设备授权校验
# if authorization(key) == True:
#     print("当前设备已授权")
# elif authorization(key) == False:
#     print("验证授权失败!")
#     print("请检查本设备是否授权!KEY是否填写正确!网络连接是否正常!")
#     print("设备码:" + str(uuid.getnode()))
#     print("==================================================")
#     if str(uuid.getnode()) != "XXXXXXXX":
#         input("请按回车键退出")
#         exit()
#     else:
#         print("当前是管理员设备")
# else:
#     print("发生预料之外的问题!程序将强制终止!")
#     print("==================================================")
#     input("请按回车键退出")
#     if str(uuid.getnode()) != "150241222380359":
#         input("请按回车键退出")
#         exit()
#     else:
#         print("当前是管理员设备")

print("==================================================")
print("简易压制工具")
print("当前版本Version:X.X.X 打包时间2024/2/04")
print("当前时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print("当前设备识别码：" + str(uuid.getnode()))
print("当前预设模式为:" + mode)
print("==================================================")
# 视频压制主程序
while True:
    # 判断是否有core视频处理文件
    if os.path.exists(os.path.join(os.path.abspath("."), "core.exe")):
        # 判断输出文件夹是否存在
        if os.path.exists(os.path.join(os.path.abspath("."), "output")):
            while True:
                print("模式")
                print("1.MP4到MP4")
                print("2.MKV压制内封字幕到MP4")
                try:
                    pattern = int(input("请输入数字1或2来选择模式:"))
                    print("==================================================")
                    if pattern == 1:
                        break
                    elif pattern == 2:
                        break
                    else:
                        print("输入错误!请重新选择!")
                        print("==================================================")
                except:
                    print("==================================================")
                    print("输入错误!请重新选择!")
                    print("==================================================")
            if pattern == 2:
                print("当前压制模式:MKV压制内封字幕到MP4")
                while True:
                    try:
                        sub_index = int(input("请输入字幕轨道索引(0-9):"))
                        print("==================================================")
                        if sub_index == 0:
                            break
                        elif sub_index == 1:
                            break
                        elif sub_index == 2:
                            break
                        elif sub_index == 3:
                            break
                        elif sub_index == 4:
                            break
                        elif sub_index == 5:
                            break
                        elif sub_index == 6:
                            break
                        elif sub_index == 7:
                            break
                        elif sub_index == 8:
                            break
                        elif sub_index == 9:
                            break
                        else:
                            print("输入错误!请重新选择!")
                            print("==================================================")
                    except:
                        print("==================================================")
                        print("输入错误!请重新选择!")
                        print("==================================================")
            if pattern == 1:
                print("当前压制模式:MP4到MP4")
            elif pattern == 2:
                print("当前压制模式:MKV压制内封字幕到MP4")
                if sub_index == 0:
                    print("当前压制字幕轨道:第1条")
                elif sub_index == 1:
                    print("当前压制字幕轨道:第2条")
                elif sub_index == 2:
                    print("当前压制字幕轨道:第3条")
                elif sub_index == 3:
                    print("当前压制字幕轨道:第4条")
                elif sub_index == 4:
                    print("当前压制字幕轨道:第5条")
                elif sub_index == 5:
                    print("当前压制字幕轨道:第6条")
                elif sub_index == 6:
                    print("当前压制字幕轨道:第7条")
                elif sub_index == 7:
                    print("当前压制字幕轨道:第8条")
                elif sub_index == 8:
                    print("当前压制字幕轨道:第9条")
                elif sub_index == 9:
                    print("当前压制字幕轨道:第10条")
            filePaths = (
                input("请输入视频路径:")
                .replace('"', "")
                .replace("'", "")
                .replace("& ", "")
            )
            print("==================================================")
            while True:
                islogo = input("是否压制水印(y/n):")
                if islogo == "y":
                    break
                elif islogo == "n":
                    break
                else:
                    print("输入错误!请重新选择!")
                    print("==================================================")
            print("==================================================")
            if os.path.isdir(filePaths):
                # 获取所有文件路径
                for root, dirs, files in os.walk(filePaths):
                    for file in files:
                        # 判断格式是否正确
                        if file.find(".mkv") != -1 or file.find(".mp4") != -1:
                            file_path = os.path.join(root, file)
                            # 下面是需要的信息
                            fileDir = os.path.basename(os.path.dirname(file_path))
                            fileName = os.path.basename(file_path)
                            filePath = file_path
                            # 判断是否创建处理后文件夹
                            if os.path.exists(
                                os.path.join(os.path.abspath("."), "output\\") + fileDir
                            ):
                                pass
                            else:
                                os.mkdir(
                                    os.path.join(os.path.abspath("."), "output\\")
                                    + fileDir
                                )
                            input_video = (
                                '"'
                                + filePath.replace('"', "")
                                .replace("'", "")
                                .replace("& ", "")
                                + '"'
                            )
                            print(input_video)
                            output_video = (
                                '"'
                                + os.path.dirname(os.path.realpath(sys.argv[0]))
                                + "\output\\"
                                + fileDir
                                + "\[Invbo]"
                                + os.path.basename(
                                    filePath.replace('"', "")
                                    .replace("'", "")
                                    .replace("& ", "")
                                )
                                + '"'
                            )
                            print("开始进行处理")
                            print(
                                "当前时间："
                                + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            )
                            print("当前文件:" + input_video)
                            print("==================================================")
                            if pattern == 1:
                                mp4compress(input_video, mode, output_video, islogo)
                            elif pattern == 2:
                                output_video = output_video.replace(".mkv", ".mp4")
                                mkvcompress(
                                    input_video, sub_index, mode, output_video, islogo
                                )
                            else:
                                print("发生预料之外的错误!")
                                input("请按回车键退出!")
                                exit()
                            print("当前文件处理完毕")
                            print("==================================================")
                        else:
                            print("当前文件格式不符合要求!跳过!")
                            print("当前文件路径:" + file)
                            print("==================================================")

            else:
                # 判断格式是否正确
                if filePaths.find(".mkv") != -1 or filePaths.find(".mp4") != -1:
                    input_video = '"' + filePaths + '"'
                    output_video = (
                        '"'
                        + os.path.dirname(os.path.realpath(sys.argv[0]))
                        + "\output\[Invbo]"
                        + os.path.basename(filePaths)
                        + '"'
                    )
                    print("开始进行处理")
                    print(
                        "当前时间："
                        + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    )
                    print("当前文件:" + input_video)
                    print("==================================================")
                    if pattern == 1:
                        mp4compress(input_video, mode, output_video, islogo)
                    elif pattern == 2:
                        output_video = output_video.replace(".mkv", ".mp4")
                        mkvcompress(input_video, sub_index, mode, output_video, islogo)
                    else:
                        print("发生预料之外的错误!")
                        input("请按回车键退出!")
                        exit()
                    print("当前文件处理完毕")
                    print("==================================================")
                else:
                    print("当前文件格式不符合要求!跳过!")
                    print("当前文件路径:" + filePaths)
                    print("==================================================")
            print("全部文件处理完毕")
            print("结束时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("==================================================")
            isExit = input("按回车键继续,输入exit退出")
            print("==================================================")
            if isExit == "exit":
                exit()
        else:
            os.mkdir(os.path.join(os.path.abspath("."), "output"))
    else:
        print("==================================================")
        input("核心文件丢失!请按回车键退出")
        exit()
