import os
import re


class PD_RemoveColorWords:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory_path": ("STRING", {"default": r"G:\\download\\宫廷圣诞猫gongyan_V1"}),  # 文件夹路径
                "words_to_remove": ("STRING", {"default": ""}),  # 要删除的单词，支持换行或空行
                "words_to_add": ("STRING", {"default": ""}),  # 要添加的单词
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Result",)
    FUNCTION = "process_directory"
    CATEGORY = "PD Custom Nodes"

    def process_directory(self, directory_path, words_to_remove, words_to_add):
        try:
            if not os.path.isdir(directory_path):
                return (f"错误：目录 {directory_path} 不存在！",)

            print(f"正在处理目录: {directory_path}")

            # 支持 \n 和多行内容的解析
            words_to_remove = [word.encode('utf-8').decode('unicode_escape').strip()
                               for word in words_to_remove.split(",") if word.strip()] or None

            words_to_add = words_to_add.strip() if words_to_add.strip() else None

            if words_to_remove:
                patterns = [
                    rf'\b{re.escape(word)}(?:\s*\([^)]*\)|_[^\s,]*|\s+[^\s,]*)?\b'
                    if word != '\n' else r'\n+'
                    for word in words_to_remove
                ]
                combined_pattern = '|'.join(patterns)

            processed_files = 0
            total_files = 0
            modified_files = 0

            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.endswith('.txt'):
                        total_files += 1
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()

                            original_content = content

                            if words_to_remove:
                                content = re.sub(combined_pattern, '', content, flags=re.IGNORECASE)

                            if words_to_add:
                                content = words_to_add + " " + content.lstrip()

                            if content != original_content:
                                modified_files += 1
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(content)
                                print(f"处理完成: {file_path}")

                            processed_files += 1
                        except Exception as e:
                            print(f"跳过文件 {file_path}，错误: {e}")
                            continue

            if processed_files == 0:
                return (f"未找到符合条件的文件",)

            result_message = f"处理完成，共扫描了 {total_files} 个文件，实际修改了 {modified_files} 个文件"
            if words_to_remove:
                result_message += f"，已删除内容：{', '.join(words_to_remove)}"
            if words_to_add:
                result_message += f"，已添加单词：'{words_to_add}'"
            return (result_message,)

        except Exception as e:
            return (f"处理出错：{e}",)


import torch
from comfy.sd import CLIP
from nodes import MAX_RESOLUTION

class Empty_Line:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # 加入 forceInput=True 让字段变成可连线的输入口
                "text": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "remove_empty_lines"
    CATEGORY = "text/processing"

    def remove_empty_lines(self, text):
        cleaned_text = re.sub(r'^[\r\n]+', '', text)
        return (cleaned_text,)
    
    
from comfy.utils import ProgressBar

import os
import re
import time
from comfy.utils import ProgressBar

class PDstring_Save:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "path": ("STRING", {"default": './output/[time(%Y-%m-%d)]', "multiline": False}),
                "filename": ("STRING", {"default": "text"}),
                "filename_delimiter": ("STRING", {"default": "_"}),
                "filename_number_padding": ("INT", {"default": 4, "min": 0, "max": 9, "step": 1}),
                "file_extension": (["txt", "json", "csv", "log", "md"], {"default": "txt"}),
            },
            "hidden": {
                "prompt": "PROMPT", 
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "save_text_file"
    CATEGORY = "PowerDiffusion/IO"
    OUTPUT_NODE = True

    def save_text_file(self, text, path, filename, filename_delimiter, filename_number_padding, file_extension, prompt=None, extra_pnginfo=None, unique_id=None):
        # 处理文件扩展名
        if not file_extension.startswith('.'):
            file_extension = f".{file_extension}"
        
        # 获取ComfyUI根目录
        comfy_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # 处理路径中的时间变量
        if '[time(' in path:
            try:
                time_format = path.split('[time(')[1].split(')]')[0]
                formatted_time = time.strftime(time_format)
                path = path.replace(f'[time({time_format})]', formatted_time)
            except:
                path = path.replace('[time(%Y-%m-%d)]', time.strftime("%Y-%m-%d"))
        
        # 处理路径
        if not os.path.isabs(path):
            path = os.path.join(comfy_dir, path)
        
        path = os.path.normpath(path)
        
        # 创建目录（如果不存在）
        os.makedirs(path, exist_ok=True)

        # 生成文件名
        if filename_number_padding == 0:
            full_filename = f"{filename}{file_extension}"
        else:
            pattern = re.compile(
                f"{re.escape(filename)}{re.escape(filename_delimiter)}(\\d{{{filename_number_padding}}}){re.escape(file_extension)}"
            )
            existing_files = [f for f in os.listdir(path) if pattern.match(f)] if os.path.exists(path) else []
            
            next_num = 1
            if existing_files:
                numbers = [int(pattern.match(f).group(1)) for f in existing_files]
                next_num = max(numbers) + 1 if numbers else 1
            
            full_filename = f"{filename}{filename_delimiter}{next_num:0{filename_number_padding}}{file_extension}"
            
            # 处理可能的冲突
            while os.path.exists(os.path.join(path, full_filename)):
                next_num += 1
                full_filename = f"{filename}{filename_delimiter}{next_num:0{filename_number_padding}}{file_extension}"

        # 写入文件
        file_path = os.path.join(path, full_filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"[PDstring_Save] 文本已保存到: {file_path}")
        except Exception as e:
            error_path = os.path.join(comfy_dir, "output", "txt", f"error_{filename}{file_extension}")
            with open(error_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"[PDstring_Save] 无法保存到 {file_path}, 错误: {e}")
            print(f"[PDstring_Save] 文本已保存到备用位置: {error_path}")

        return ()

    @staticmethod
    def IS_CHANGED(*args, **kwargs):
        return float("NaN")

# 节点映射
NODE_CLASS_MAPPINGS = {
    "PD_RemoveColorWords": PD_RemoveColorWords,
    "Empty_Line": Empty_Line,
    "PDstring_Save": PDstring_Save,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PD_RemoveColorWords": "PD_批量去除/添加单词",
    "Empty_Line": "PDstring:del_EmptyLine",
    "PDstring_Save": "PDstring:txtSave",
}
