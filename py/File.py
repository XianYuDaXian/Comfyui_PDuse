import os
import comfy.utils

class FileName_refixer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": ""}),
                "prefix": ("STRING", {"default": "TL"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result_info",)
    FUNCTION = "add_prefix"
    CATEGORY = "ZHO Tools"

    def add_prefix(self, folder_path, prefix="TL"):
        result = {
            "success": [],
            "errors": [],
            "total_processed": 0
        }
        
        if not os.path.exists(folder_path):
            return (f"Error: Folder path does not exist - {folder_path}",)
            
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                if os.path.isfile(file_path):
                    # 分离文件名和扩展名
                    name, ext = os.path.splitext(filename)
                    
                    # 构建新文件名
                    new_name = f"{prefix}{name}{ext}"
                    new_path = os.path.join(folder_path, new_name)
                    
                    try:
                        os.rename(file_path, new_path)
                        result["success"].append({
                            "original": filename,
                            "new_name": new_name
                        })
                        result["total_processed"] += 1
                    except Exception as e:
                        result["errors"].append({
                            "filename": filename,
                            "error": str(e)
                        })
            
            # 构建结果信息
            success_count = len(result["success"])
            error_count = len(result["errors"])
            
            report = f"Operation completed\nSuccess: {success_count}\nErrors: {error_count}"
            
            if success_count > 0:
                report += "\n\nSuccessfully renamed files:\n"
                report += "\n".join([f" - {item['original']} → {item['new_name']}" for item in result["success"]])
            
            if error_count > 0:
                report += "\n\nErrors occurred:\n"
                report += "\n".join([f" - {item['filename']}: {item['error']}" for item in result["errors"]])
            
            return (report,)
                
        except Exception as e:
            return (f"Critical error: {str(e)}",)

# 在 ComfyUI 中的节点映射配置
NODE_CLASS_MAPPINGS = {"PDFile_FileName_refixer": FileName_refixer}
# 设置节点在 UI 中显示的名称
NODE_DISPLAY_NAME_MAPPINGS = {"PDFile_FileName_refixer": "PDFile_Name_refixer"} # 自定义节点名称

