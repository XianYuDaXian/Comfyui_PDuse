import os
import re


class PD_RemoveColorWords:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory_path": ("STRING", {"default": r"G:\download\宫廷圣诞猫gongyan_V1"}),  # 文件夹路径
                "words_to_remove": ("STRING", {"default": ""}),  # 要删除的单词（可为空）
                "words_to_add": ("STRING", {"default": ""}),  # 要添加的单词（可为空）
            },
        }

    RETURN_TYPES = ("STRING",)  # 输出为字符串类型，用于返回操作结果
    RETURN_NAMES = ("Result",)  # 返回值的名称
    FUNCTION = "process_directory"  # 指定执行的方法名称
    CATEGORY = "PD Custom Nodes"  # 定义节点的类别，便于分类

    def process_directory(self, directory_path, words_to_remove, words_to_add):
        try:
            # 确保目录路径有效
            if not os.path.isdir(directory_path):
                return (f"错误：目录 {directory_path} 不存在！",)

            print(f"正在处理目录: {directory_path}")

            # 处理要删除的单词
            words_to_remove = [word.strip() for word in words_to_remove.split(",") if word.strip()] or None

            # 处理要添加的单词
            words_to_add = words_to_add.strip() if words_to_add.strip() else None

            # 构建正则表达式（如果 `words_to_remove` 存在）
            if words_to_remove:
                regex_pattern = r'\b(' + '|'.join(re.escape(word) for word in words_to_remove) + r')\b'

            processed_files = 0  # 统计处理的文件数

            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    # 确保只处理.txt文件
                    if not file.lower().endswith('.txt'):
                        continue
                        
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # 如果 `words_to_remove` 存在，删除指定单词
                        if words_to_remove:
                            content = re.sub(regex_pattern, '', content, flags=re.IGNORECASE)

                        # 如果 `words_to_add` 存在，添加新单词到文件开头
                        if words_to_add:
                            content = words_to_add + "\n" + content

                        # 写回修改后的内容
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)

                        print(f"处理完成: {file_path}")
                        processed_files += 1
                    except UnicodeDecodeError:
                        print(f"跳过文件 {file_path}，不是有效的UTF-8文本文件")
                        continue
                    except Exception as e:
                        print(f"跳过文件 {file_path}，错误: {e}")
                        continue

            if processed_files == 0:
                return ("未找到符合条件的.txt文件",)

            result_message = f"处理完成，共处理了 {processed_files} 个.txt文件"
            if words_to_remove:
                result_message += f"，已删除单词：{', '.join(words_to_remove)}"
            if words_to_add:
                result_message += f"，已添加单词：'{words_to_add}'"
            return (result_message,)

        except Exception as e:
            return (f"处理出错：{e}",)


# 节点映射
NODE_CLASS_MAPPINGS = {
    "PD_RemoveColorWords": PD_RemoveColorWords,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PD_RemoveColorWords": "PD_批量去除/添加单词",
}