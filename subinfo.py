import re
import subprocess
import os
import sys
import time


def match_subtitle_info(text):
    pattern = r"Stream #\d+.*Subtitle:.*?(?=Stream #|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


# 查看视频字幕轨道
def subinfo(input_video):
    command = f"core.exe -i {input_video}"
    try:
        # 执行命令并获取输出
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode(
            "utf-8"
        )
    except subprocess.CalledProcessError as e:
        output = e.output.decode("utf-8")
        regex = r"(Stream #\d+:\d+\(.*?\): Subtitle: .*?\n)([\s\S]*?\n){2}"
        matches = re.finditer(regex, output)
        index = -1
        for match in matches:
            index = index + 1
            print("字幕索引:第" + str(index) + "个")
            output = match.group(0)
            lines = output.splitlines()
            if len(lines) > 1:
                lines.pop(1)  # 删除第二行
            result = (
                "\n".join(lines)
                .replace(" ", "")
                .replace("Subtitle:", "")
                .replace("title", "字幕标题")
            )
            print(result)
            print("==================================================")


# 切换工作目录
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
print("==================================================")
print("MKV字幕轨道查看工具")
print("当前版本Version:X.X.X 打包时间2024/2/01")
print("当前时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print("==================================================")
# 判断是否有core视频处理文件
if os.path.exists(os.path.join(os.path.abspath("."), "core.exe")):
    while True:
        filePaths = (
            input("请输入视频路径:").replace('"', "").replace("'", "").replace("& ", "")
        )
        # 判断格式是否正确
        if filePaths.find(".mkv") != -1:
            print("==================================================")
            input_video = '"' + filePaths + '"'
            subinfo(input_video)
            isexit = input("按回车继续,输入exit退出")
            if isexit == "exit":
                break
            print("==================================================")
        else:
            print("输入文件不是MKV!跳过!")
            print("==================================================")
else:
    print("核心文件丢失!")
    input("请按回车键退出")
    exit()
