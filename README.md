# Music_to_lrc-MTR


通过音乐提取出对应的LRC歌词文件

## 使用前准备


1.安装ffmpeg
```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```
2.安装openai-whisper

```
pip install -U openai-whisper
```


3.(可选)安装openai 对于歌词自动格式化
```
pip install openai
```

## 使用方法

克隆源代码或下载MTR.exe
在命令行中：
```
MTR --target target_file --model model_type --af True/False （可选） --key chatgpt_api_key （可选）
```

使用帮助：
```
MTR --help
```
## 使用效率与准确率

```
测试平台：
处理器：AMD Ryzen 5 5500
显卡: RTX2060
内存: 20G DDR4 3200 (16+4)
CUDA版本:11.0
操作系统：Windows11 PRO 22H2
```

测试歌曲名单：

1.Edge of my life
![image](https://github.com/istrashguy/Music_to_lrc-MTR/assets/110215026/4be9d82a-54d4-48fe-a9c5-deb299fe94cc)

2.Bet on me
![image](https://github.com/istrashguy/Music_to_lrc-MTR/assets/110215026/92442952-fb2d-40a4-bc65-4a8983a38b49)


3.Xin Đừng Nhấc Máy (Remix)
测试失败

4.只因你太美
![image](https://github.com/istrashguy/Music_to_lrc-MTR/assets/110215026/feca5f3c-06cc-48d3-a197-688b4154bbda)


模型选择：medium
歌曲格式：M4A

英语歌曲Edge of my life 整体准确率为60%以上(大概?)
Bet on me 50%以上

Xin Đừng Nhấc Máy (Remix) 作为越南语与英语结合的歌曲无法被识别(不知道指定语言行不行)

只因你太美 作为中文压轴歌曲，不负众望，30%左右的准确率

## 免责声明

音乐转文字服务由Openai's Whisper提供，准确性无法保证，模型准确率取决于电脑硬件配置

Whisper仓库地址：https://github.com/openai/whisper/

