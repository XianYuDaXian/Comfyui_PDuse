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

            # 如果 `words_to_remove` 是空字符串或仅包含空格，则设置为 None
            words_to_remove = [word.strip() for word in words_to_remove.split(",") if word.strip()] or None

            # 如果 `words_to_add` 是空字符串或仅包含空格，则跳过添加
            words_to_add = words_to_add if words_to_add.strip() else None

            # 修改正则表达式的构建方式
            if words_to_remove:
                regex_pattern = r'\b(' + '|'.join(
                    re.escape(word) + r'(?:\s*\([^)]*\)|\s*_[^\s,]*|\s+\([^)]*\)|\s+[^\s,]*)?'
                    for word in words_to_remove
                ) + r')\b'

            processed_files = 0  # 统计处理的文件数
            total_files = 0  # 统计扫描的文件总数
            modified_files = 0  # 统计实际修改的文件数

            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.endswith('.txt'):
                        total_files += 1
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            original_content = content  # 保存原始内容以便比较

                            # 如果 `words_to_remove` 存在，删除指定单词
                            if words_to_remove:
                                for word in words_to_remove:
                                    # 分别处理不同的模式
                                    patterns = [
                                        rf'\b{re.escape(word)}\s*\([^)]*\)',  # 匹配 "PD (style)"
                                        rf'\b{re.escape(word)}_[^\s,]*',      # 匹配 "PD_style"
                                        rf'\b{re.escape(word)}\b'             # 匹配单独的 "PD"
                                    ]
                                    for pattern in patterns:
                                        content = re.sub(pattern, '', content, flags=re.IGNORECASE)

                            # 如果 `words_to_add` 存在，添加新单词到文件开头
                            if words_to_add:
                                content = words_to_add + "\n" + content

                            # 检查内容是否有变化
                            if content != original_content:
                                modified_files += 1
                                # 写回修改后的内容
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
