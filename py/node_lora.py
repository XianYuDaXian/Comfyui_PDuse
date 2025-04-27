import os
import re
from collections import Counter

class ReadTxtFiles:
    """
    读取指定文件夹中所有txt文件的节点，并统计颜色词和高频词
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {
                    "default": "./", 
                    "multiline": False
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_text",)
    FUNCTION = "read_txt_files"
    CATEGORY = "文件操作"

    def get_color_words(self, text):
        """
        提取文本中的颜色词
        """
        # 要删除的颜色词列表 - 这些颜色词不会在统计结果中显示
        remove_colors = {
            # 红色系 'red', 'soft','crimson', 'scarlet', 'maroon', 'burgundy', 'ruby', 'cherry',
            
        }
        
        # 扩充的颜色词列表
        color_words = [
            # 英文基础颜色
            'red', 'blue', 'green', 'yellow', 'purple', 'orange', 
            'brown', 'pink', 'golden', 'silver', 'cyan', 'magenta',
            
            # 英文深浅色调
            'light', 'pale', 'deep', 'bright', 'vivid', 'soft',
            
            # 英文具体颜色描述
            # 红色系
            'crimson', 'scarlet', 'maroon', 'burgundy', 'ruby', 'cherry', 'wine',
            'carmine', 'vermillion', 'cardinal', 'russet', 'garnet',
            
            # 蓝色系
            'navy', 'azure', 'cobalt', 'indigo', 'turquoise', 'teal', 'sapphire',
            'cerulean', 'aqua', 'aquamarine', 'ultramarine', 'royal blue',
            
            # 绿色系
            'emerald', 'olive', 'lime', 'sage', 'forest', 'mint', 'jade',
            'viridian', 'chartreuse', 'seafoam', 'shamrock', 'malachite',
            
            # 黄色系
            'amber', 'gold', 'honey', 'lemon', 'canary', 'mustard', 'saffron',
            'butterscotch', 'dandelion', 'flaxen', 'marigold',
            
            # 紫色系
            'violet', 'lavender', 'mauve', 'lilac', 'plum', 'amethyst',
            'orchid', 'mulberry', 'periwinkle', 'heliotrope',
            
            # 粉色系
            'coral', 'salmon', 'peach', 'rose', 'fuchsia', 'cerise',
            'flamingo', 'blush', 'bubblegum', 'watermelon',
            
            # 橙色系
            'tangerine', 'apricot', 'persimmon', 'rust', 'ginger', 'cinnamon',
            
            # 中文基础颜色
            '红', '蓝', '绿', '黄', '紫', '橙', '棕', '粉', '金', '银', '青', '橘',
            
            # 中文深浅色调
            '浅', '深', '淡', '亮', '鲜', '素', '纯',
            
            # 中文具体颜色描述
            # 红色系
            '赤', '绯', '殷红', '血红', '朱红', '火红', '丹红', '粉红', '桃红', '玫瑰红',
            '胭脂', '珊瑚', '枣红', '樱桃红', '红棕', '砖红', '艳红',
            
            # 蓝色系
            '湖蓝', '天蓝', '海蓝', '靛青', '靛蓝', '宝蓝', '蔚蓝', '群青',
            '孔雀蓝', '碧蓝', '水蓝', '湛蓝', '青金石蓝',
            
            # 绿色系
            '草绿', '墨绿', '葱绿', '柳绿', '松绿', '橄榄绿', '青翠', '碧绿', '翠绿',
            '苔绿', '豆绿', '玉绿', '竹青', '嫩绿', '翡翠绿',
            
            # 黄色系
            '金黄', '橙黄', '杏黄', '雅黄', '鹅黄', '鸭黄', '柠檬黄', '姜黄',
            '蜜黄', '芥末黄', '秋黄', '杭黄', '璨黄',
            
            # 紫色系
            '紫罗兰', '茄紫', '葡萄紫', '丁香紫', '青莲', '紫酱', '酱紫',
            '雪青', '藕荷', '紫水晶', '贵妃紫', '紫檀',
            
            # 特殊颜色描述
            '彩虹色', '渐变', '多彩', '五彩', '七彩', '斑斓', '炫彩',
            'rainbow', 'gradient', 'multicolor', 'iridescent', 'prismatic',
            'opalescent', 'holographic', 'psychedelic', 'kaleidoscopic',
            
            # 金属色
            '铜色', '铂金色', '玫瑰金', '珠光',
            'metallic', 'chrome', 'platinum', 'rose gold', 'pearlescent',
            'copper', 'bronze', 'brass', 'iridescent'
        ]
        
        found_colors = []
        text_lower = text.lower()
        
        # 检查完整词
        for color in color_words:
            if color.lower() in text_lower:
                found_colors.append(color)
            
        # 检查颜色组合（例如：light blue, 深蓝色）
        for modifier in ['light', 'pale', 'deep', 'bright', 'soft', '浅', '深', '淡', '亮', '鲜']:
            for color in color_words:
                combined = f"{modifier} {color}"
                if combined.lower() in text_lower:
                    found_colors.append(combined)
                # 检查中文组合
                combined_cn = f"{modifier}{color}"
                if combined_cn in text_lower:
                    found_colors.append(combined_cn)
        
        return list(set(found_colors))  # 去重

    def get_top_words(self, text, top_n=5):
        """
        获取文本中出现频率最高的词
        """
        # 分词（这里使用简单的空格分词，可以根据需要改进）
        words = re.findall(r'\w+', text.lower())
        # 过滤掉长度为1的词
        words = [word for word in words if len(word) > 1]
        # 统计词频
        word_counts = Counter(words)
        # 返回最常见的n个词
        return word_counts.most_common(top_n)

    def read_txt_files(self, folder_path: str) -> tuple[str]:
        """
        读取指定文件夹中的所有txt文件
        
        Args:
            folder_path (str): 文件夹路径
            
        Returns:
            tuple[str]: 格式化后的所有文件内容
        """
        try:
            if not os.path.exists(folder_path):
                return (f"错误: 文件夹 '{folder_path}' 不存在",)

            # 获取所有txt文件
            txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
            
            if not txt_files:
                return ("未找到txt文件: 文件夹中没有txt文件",)

            # 存储所有文件内容
            all_contents = []
            all_text = ""  # 用于统计的完整文本

            # 读取每个文件
            for file_name in txt_files:
                file_path = os.path.join(folder_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        all_text += content + " "
                        
                    # 格式化文件信息
                    all_contents.append(
                        f"\n{'='*50}\n"
                        f"文件名: {file_name}\n"
                        f"{'='*50}\n"
                        f"{content}\n"
                    )
                except Exception as e:
                    all_contents.append(
                        f"\n{'='*50}\n"
                        f"文件名: {file_name}\n"
                        f"读取失败: {str(e)}\n"
                        f"{'='*50}\n"
                    )

            # 统计信息
            color_words = self.get_color_words(all_text)
            top_words = self.get_top_words(all_text)
            
            # 格式化统计信息
            stats = (
                f"\n{'='*50}\n"
                f"统计信息:\n"
                f"文件数量: {len(txt_files)}个\n"
                f"出现的颜色词: {', '.join(color_words) if color_words else '无'}\n"
                f"出现频率最高的5个单词: {', '.join([f'{word}({count}次)' for word, count in top_words])}\n"
                f"{'='*50}"
            )

            # 合并所有信息
            return ("".join(all_contents) + stats,)

        except Exception as e:
            return (f"处理文件时发生错误: {str(e)}",)

# 注册节点
NODE_CLASS_MAPPINGS = {
    "ReadTxtFiles": ReadTxtFiles,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ReadTxtFiles": "PD_ReadTxtFiles", # 新添加的节点
}
