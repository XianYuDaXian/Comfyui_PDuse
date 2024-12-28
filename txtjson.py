import os
import re


class PD_RemoveColorWords:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory_path": ("STRING", {"default": r"G:\download\宫廷圣诞猫gongyan_V1"}),  # 文件夹路径
                "words_to_remove": ("STRING", {"default": "red,gold,white"}),  # 要删除的颜色单词
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Result",)
    FUNCTION = "remove_words_in_directory"
    CATEGORY = "PD Custom Nodes"

    def remove_words_in_directory(self, directory_path, words_to_remove):
        try:
            # 确保目录路径有效
            if not os.path.isdir(directory_path):
                return (f"错误：目录 {directory_path} 不存在！",)

            print(f"正在处理目录: {directory_path}")
            words = [word.strip() for word in words_to_remove.split(",")]
            regex_pattern = r'\b(' + '|'.join(re.escape(word) for word in words) + r')\b'

            processed_files = 0  # 统计处理的文件数
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            new_content = re.sub(regex_pattern, '', content, flags=re.IGNORECASE)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            print(f"处理完成: {file_path}")
                            processed_files += 1
                        except Exception as e:
                            print(f"跳过文件 {file_path}，错误: {e}")
                            continue

            if processed_files == 0:
                return (f"未找到符合条件的文件",)
            return (f"处理完成，共处理了 {processed_files} 个文件，已删除单词：{', '.join(words)}",)
        except Exception as e:
            return (f"处理出错：{e}",)


# 节点映射
NODE_CLASS_MAPPINGS = {
    "PD_RemoveColorWords": PD_RemoveColorWords,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PD_RemoveColorWords": "PD_批量去除文本字体",
}
