import os
import json


class BatchChangeNodeColor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory_path": ("STRING", {"default": r"A:\path\to\json_files"}),  # JSON 文件夹路径
                "color_choice": (["Blue", "DeepGray", "Yellow", "Green"],),  # 提供颜色选择
            },
        }

    RETURN_TYPES = ("STRING",)  # 输出为字符串类型，用于返回操作结果
    RETURN_NAMES = ("Result",)
    FUNCTION = "batch_change_color"  # 指定要执行的方法名称
    CATEGORY = "PD Custom Nodes"  # 自定义类别

    def batch_change_color(self, directory_path, color_choice):
        try:
            # 根据选择的颜色设置目标颜色值
            color_map = {
                "Blue": "#3f789e",  # 蓝色
                "DeepGray": "#444",  # 深灰色
                "Yellow": "#c09430",  # 黄色
                "Green": "#3c763d",  # 绿色
            }
            target_color = color_map.get(color_choice, "#444")  # 默认深灰色

            # 遍历目标文件夹
            for root, _, files in os.walk(directory_path):
                for file in files:
                    if file.endswith(".json"):
                        file_path = os.path.join(root, file)
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)

                        # 遍历 JSON 的 groups 部分并修改颜色
                        groups = data.get("groups", [])
                        for group in groups:
                            group["color"] = target_color

                        # 保存修改后的 JSON 文件
                        with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)

                        print(f"已处理文件：{file_path}")

            return (f"所有 JSON 文件已成功修改为颜色：{color_choice} ({target_color})",)

        except Exception as e:
            return (f"处理出错：{e}",)


# 添加到节点映射中
NODE_CLASS_MAPPINGS = {
    "BatchChangeNodeColor": BatchChangeNodeColor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchChangeNodeColor": "批量修改节点颜色",
}
