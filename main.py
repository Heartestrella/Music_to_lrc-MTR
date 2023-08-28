# -*- coding: utf-8 -*-

import os
import argparse
import re
import argparse
import openai
import warnings

def custom_formatwarning(msg, *args, **kwargs):
    return "\x1b[1;31mWarning: {}\x1b[0m\n".format(str(msg))

def text_to_lrc(detected_language, lrc_text):
    start_time = "00:00.000"

    matches = re.findall(r"\[.*?\]", lrc_text)
    if len(matches) >= 2:
        content = matches[1][1:-1]
        end_time = f"[{content}]"[1:10]
    timestamp = f"[{start_time} --> {end_time}]"
    lrc_text = f"{timestamp}  {lrc_text}"

    lrc_list = []
    lrc_ = []
    timestamps = []
    for i in lrc_text:
        if i == "\n":
            lrc_str = "".join(lrc_list[27:])
            timestamp = "".join(lrc_list[:26])
            text_list = list(timestamp)
            text_list[3] = ":"
            modified_text = "".join(text_list)
            timestamps.append(modified_text)
            lrc_.append(lrc_str)
            lrc_list.clear()
            timestamp = ""
        else:
            lrc_list.append(i)
    lrc_content = ""
    for lrc, timestamp in zip(lrc_, timestamps):
        text = f"[{timestamp[1:9]}]{lrc} \n"
        lrc_content += text

    return lrc_content


def format_lrc_with_gpt(lrc_content):
    prompt = f"Format the following lrc lyrics:\n{lrc_content}\n\nBreak the lyrics into appropriate lines and provide timings for each line:\n"

    response = openai.Completion.create(
        engine="davinci", prompt=prompt, temperature=0.7, max_tokens=2049
    )

    if response.choices:
        formatted_lyrics = response.choices[0].text.strip()
        return formatted_lyrics
    else:
        return "API request failed"


def main():
    parser = argparse.ArgumentParser(description="Command line argument example")

    parser.add_argument(
        "--target", type=str, help="输入的目标文件名，可输入类型详见：https://github.com/openai/whisper/"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="传入模型类型，详见: https://github.com/openai/whisper/ ",
        default="base",
    )
    parser.add_argument("--af", type=bool, default=False, help="这个方法由Chatgpt提供格式化功能")
    parser.add_argument(
        "--key",
        type=str,
        default="",
        help="如果自动格式化设定为Ture，请设定Chatgpt api key，此key只用于格式化歌词，不会用于其他用途",
    )

    args = parser.parse_args()

    target, model, auto_format, api_key = args.target, args.model, args.af, args.key
    if auto_format == True:
        if 'sk-' in api_key:
            openai.api_key = api_key
        else:
            raise ValueError("请给定API KEY值或修正API KEY值")

    shell = f"whisper {target} -f txt --model {model}"
    os.system(f"{shell} > output.txt")
    try:
        with open("output.txt", mode="r", encoding="ANSI") as r:
            output_shell = r.read()
    except: 
        with open("output.txt", mode="r", encoding="UTF-8") as r:
            output_shell = r.read()
    os.remove("output.txt")
    language_pattern = r"Detected language: (\w+)"
    text_pattern = r"\[.*?\] (.+?)(?=\n\[[\d:.]+\]|$)"

    language_match = re.search(language_pattern, output_shell)
    text_matches = re.findall(text_pattern, output_shell, re.DOTALL)

    if language_match and text_matches:
        detected_language = language_match.group(1)


        for i, extracted_text in enumerate(text_matches):
            lrc_text = ""
            lrc_text += extracted_text.strip()
    else:
        raise ValueError('未能识别出任何歌词或语言')

    lrc_content = text_to_lrc(detected_language, lrc_text)
    if auto_format == True:
        if len(lrc_content) < 2048:
            lrc_content = format_lrc_with_gpt(lrc_content)
        else:
            warnings.formatwarning = custom_formatwarning
            warnings.warn("字符串长度超出GPT-3.5模型长度限制，请尝试更换GPT4.0或手动将LRC复制到网页端GPT进行格式化", UserWarning)
    with open(target + ".lrc", mode="w", encoding="UTF-8") as w:
        w.write(lrc_content)



if __name__ == "__main__":
    main()
