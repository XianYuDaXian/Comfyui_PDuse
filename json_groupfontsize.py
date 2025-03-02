import json
import os  # 用于路径和文件操作  
#
class json_group_fontsize:   # 定义一个名为 MyNode 的类，表示自定义节点
    def __init__(self):
        pass
     
      # 定义一个类方法，用于指定节点的输入类型
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {   # 定义必要的输入参数
                "input_folder_path": ("STRING", {"default":r"A:\1_area\area_python\pojie"}), # 输入文件路径   # 参数名为 text，类型为字符串，默认值为 "Hey Hey!"
                "output_folder_path": ("STRING", {"default": r"A:\1_area\area_python\outputpy"}),
                "new_file_name": ("STRING", {"default": "新工作流"}),  # 新的 JSON 文件名称（支持中文）
                "title": ("STRING", {"default": "TL_一键白底_V1"}),  # 指定需要保持 font_size 不变的 title
                "font_size": ("INT", {"default": 60}),  # 需要统一修改的 fmodified.jsonont_size 值	 
            },
        }


    # 定义节点的返回值类型和名称
    RETURN_TYPES = ("STRING",)  # 输出为字符串类型
    RETURN_NAMES = ("Processed_Files",)  # 输出的名称为 "Processed_Files"

    # 定义节点的功能函数名
    FUNCTION = "process_json_files"

    CATEGORY = "image/PD_use"   # 定义节点类别，显示在 ComfyUI 的节点分类中

    def process_json_files(self, input_folder_path, output_folder_path, new_file_name, title, font_size):
        try:
            # 自动规范路径，解决反斜杠问题
            input_folder_path = os.path.normpath(input_folder_path)
            output_folder_path = os.path.normpath(output_folder_path)
        

            # 打印调试信息
            print(f"Input folder: {input_folder_path}")
            print(f"Output folder: {output_folder_path}")

            # 检查输入文件夹是否存在
            if not os.path.exists(input_folder_path):
                return (f"Error: 输入文件夹路径不存在: {input_folder_path}",)

            # 检查输出文件夹是否存在
            if not os.path.exists(output_folder_path):
                os.makedirs(output_folder_path)

            # 获取输入文件夹中的所有文件
            all_files = os.listdir(input_folder_path)
            print(f"All files in folder: {all_files}")

            # 查找 .json 文件
            json_files = [f for f in all_files if f.lower().endswith(".json")]
            print(f"Found JSON files: {json_files}")

            # 如果没有找到 .json 文件，打印错误信息并返回
            if not json_files:
                print(f"Error: 输入文件夹中没有找到 JSON 文件: {input_folder_path}")
                return (f"Error: 输入文件夹中没有找到 JSON 文件: {input_folder_path}",)

            processed_files = []  # 用于记录已处理的文件路径
            
            #  自动添加 .json 后缀，
            if not new_file_name.endswith(".json"):
                new_file_name += ".json"

            # 遍历 JSON 文件
            for index, json_file in enumerate(json_files, start=1):  # 从 1 开始计数
                input_file_path = os.path.join(input_folder_path, json_file)
                output_file_name = f"{new_file_name}_{index}.json"  # 按顺序命名输出文件
                output_file_path = os.path.join(output_folder_path, output_file_name)
                #使用 enumerate(json_files, start=1) 生成文件索引。
                # 构造输出文件名为 f"{new_file_base_name}_{index}.json"。
                print(f"正在处理文件：{input_file_path}")

                # 读取 JSON 文件
                try:
                    with open(input_file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON file {input_file_path}: {e}")
                    continue

                # 修改 JSON 数据
                for group in data.get("groups", []):
                    
                    old_font_size = group.get("font_size", "未定义")   # 获取旧的字体大小，
                    # 如果组的 title 不匹配，则修改 font_size
                    if group.get("title") != title:  # 如果组的 title 不匹配，则修改 font_size
                        group["font_size"] = font_size
                        print(f"已修改组: {group.get('title')} | Font size: {old_font_size} -> {font_size}")
                    else:
                            print(f"跳过组：'{group.get('title')}'，字体大小保持为：{group.get('font_size')}")

                # 保存修改后的 JSON 数据
                with open(output_file_path, 'w', encoding='utf-8') as f: #为使用 open 函数以写模式 ('w') 打开文件时，会自动覆盖已有文件。
                    json.dump(data, f, ensure_ascii=False, indent=4)

                print(f"文件已覆盖并保存到：{output_file_path}")
                processed_files.append(output_file_path)

            # 返回处理过的文件列表
            return (f"修改完成！已处理的文件保存在目录：{output_folder_path}\n文件列表：{', '.join(processed_files)}",)
        except Exception as e:
            # 返回错误信息
            return (f"Error: {e}",)

# 定义一个字典，包含所有需要导出的节点及其名称
NODE_CLASS_MAPPINGS = {
    "json_group_fontsize": json_group_fontsize   # 将 "My First Node" 映射到 MyNode 类，告诉系统应该用哪个类来实现这个节点的逻辑。
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {  
    "json_group_fontsize": "json_group_fontsize"   # 将内部名称 "FirstNode" 映射为显示名称 "My First Node"
}
