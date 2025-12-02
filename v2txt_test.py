from asyncio.windows_events import NULL
from stslib import cfg, tool
from faster_whisper import WhisperModel
import re
import os
import time
from openai import OpenAI
from gruut import sentences
from allosaurus.app import read_recognizer
import ctypes  # An included library with Python install.
import pymsgbox
from openai import OpenAI

def v2s(input_path=None):
    model = read_recognizer()
    syllables2 = model.recognize(input_path)
    syllables2 = syllables2.replace(" ", "")
    print(syllables2)
    return syllables2

def shibie(model=None, language=None, data_type=None, wav_file=None):
    key = "placeholder"
    try:
        sets = cfg.parse_ini()
        cfg.progressbar[key] = 0
        print(f'{model=}')

        try:
            modelobj = WhisperModel(
                model if not model.startswith(
                    'distil') else model.replace('-whisper', ''),
                device='cpu',
                local_files_only = False,
                cpu_threads=32,
                compute_type=sets.get('cuda_com_type'),
                download_root=cfg.ROOT_DIR + "/models"
            )
        except Exception as e:
            err = f'从huggingface.co下载模型 {model} 失败，请检查网络连接' if model.find(
                '/') > 0 else ''
            cfg.progressresult[key] = 'error:'+err+str(e)
            return

        segments, info = modelobj.transcribe(
            wav_file,
            beam_size=sets.get('beam_size'),
            best_of=sets.get('best_of'),
            # temperature=0 if sets.get('temperature')==0 else [0.0,0.2,0.4,0.6,0.8,1.0],
            condition_on_previous_text=sets.get('condition_on_previous_text'),
            vad_filter=sets.get('vad'),
            # vad_parameters=dict(
            #    min_silence_duration_ms=300
            # ),
            language=language if language != 'auto' else None,
            initial_prompt=sets.get(
                'initial_prompt_zh') if language == 'zh' else None
        )
        # Same precision as the Whisper timestamps.
        total_duration = round(info.duration, 2)

        raw_subtitles = []
        for segment in segments:
            cfg.progressbar[key] = round(segment.end/total_duration, 2)
            start = int(segment.start * 1000)
            end = int(segment.end * 1000)
            startTime = tool.ms_to_time_string(ms=start)
            endTime = tool.ms_to_time_string(ms=end)
            text = segment.text.strip().replace('&#39;', "'")
            text = re.sub(r'&#\d+;', '', text)

            # 无有效字符
            if not text or re.match(r'^[，。、？‘’“”；：（｛｝【】）:;"\'\s \d`!@#$%^&*()_+=.,?/\\-]*$', text) or len(
                    text) <= 1:
                continue
            if data_type == 'json':
                # 原语言字幕
                raw_subtitles.append(
                    {"line": len(raw_subtitles) + 1, "start_time": startTime, "end_time": endTime, "text": text})
            elif data_type == 'text':
                raw_subtitles.append(text)
            else:
                raw_subtitles.append(
                    f'{len(raw_subtitles) + 1}\n{startTime} --> {endTime}\n{text}\n')
        cfg.progressbar[key] = 1
        if data_type != 'json':
            raw_subtitles = "\n".join(raw_subtitles)
        cfg.progressresult[key] = raw_subtitles
        # print(raw_subtitles)
        return raw_subtitles
    except Exception as e:
        cfg.progressresult[key] = 'error:'+str(e)
        print(str(e))

input_dir = "tmp"
output_dir = "outputs"
for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            # 输入文件的完整路径
            input_path = os.path.join(root, file_name)

            # 构造输出路径：保持目录结构，替换扩展名为.txt
            relative_path = os.path.relpath(input_path, input_dir)
            output_file = os.path.splitext(relative_path)[0] + '.txt'
            output_path = os.path.join(output_dir, output_file)

            # 创建输出目录（如果不存在）
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            prompt = "有一名非英文母语的学生录了一段英文的音频。用whisper的large, medium, small, base, tiny分别转出了以下逐字稿，并用allosaurus.app转出了以下音频对应的音标。由于模型越小，对于发音错误的单词的识别越差，请根据以下逐字稿和音标分析其可能发音不正确的单词（学生的回答可能有语法错误，需要忽略因语法错误而错的单词）："
            prompt += "large: \n" + shibie("large", "auto", "text", input_path) + "\n\n"
            prompt += "medium: \n" + shibie("medium", "auto", "text", input_path) + "\n\n"
            prompt += "small: \n" + shibie("small", "auto", "text", input_path) + "\n\n"
            prompt += "base: \n" + shibie("base", "auto", "text", input_path) + "\n\n"
            prompt += "tiny: \n" + shibie("tiny", "auto", "text", input_path) + "\n\n用allosaurus.app转出的音频对应的音标：\n"
            prompt += v2s(input_path)

            client = OpenAI(api_key="INSERT-API-KEY-HERE", base_url="https://api.deepseek.com")

            response = client.chat.completions.create(model="deepseek-chat", messages=[
                                    {"role": "system", "content": "You are a helpful assistant"},
                                    {"role": "user", "content": prompt},],stream=False
            )

            print(response.choices[0].message.content)

            with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(response.choices[0].message.content)