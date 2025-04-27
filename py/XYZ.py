# ModelParamLoader.py
import os
import folder_paths
import torch
from comfy.sd import load_lora_for_models
from comfy.utils import load_torch_file

class LoRALoader_path:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "lora_path": ("STRING", {"default": "", "placeholder": "输入LoRA文件完整路径(如E:/models/lora.safetensors)"}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -2.0, "max": 2.0, "step": 0.1}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -2.0, "max": 2.0, "step": 0.1}),
            },
            "optional": {
                "clip": ("CLIP", {"default": None}),
                "flux_mode": ("BOOLEAN", {"default": False})
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP")
    RETURN_NAMES = ("model", "clip")
    FUNCTION = "load_lora"
    CATEGORY = "PD_Nodes/Loaders"

    def load_lora(self, model, lora_path, strength_model, strength_clip, clip=None, flux_mode=False):
        try:
            # 增强型路径验证
            lora_path = self.validate_lora_path(lora_path)
            
            # 文件内容验证
            if not self.is_valid_lora(lora_path):
                raise ValueError("文件内容不符合LoRA格式要求")
                
            # 实际加载逻辑
            return self._actually_load_lora(model, clip, lora_path, strength_model, strength_clip, flux_mode)
            
        except Exception as e:
            self.generate_debug_report(lora_path)
            raise ValueError(f"LoRA加载失败(深度诊断): {str(e)}")

    def validate_lora_path(self, path):
        """增强型路径验证"""
        path = os.path.abspath(os.path.normpath(path))
        
        # 检查文件扩展名
        if not path.lower().endswith(('.safetensors', '.ckpt')):
            raise ValueError("仅支持.safetensors或.ckpt格式")
            
        # 检查文件大小
        if os.path.getsize(path) < 1024:  # 小于1KB肯定是无效文件
            raise ValueError("文件大小异常，可能已损坏")
            
        return path

    def is_valid_lora(self, path):
        """验证文件内容是否为有效LoRA"""
        try:
            # 快速检查文件头
            with open(path, 'rb') as f:
                header = f.read(16)
                if b'safetensors' not in header and b'ckpt' not in header:
                    return False
                    
            # 尝试加载元数据
            temp = load_torch_file(path, safe_load=True)
            return 'lora' in str(temp.keys()).lower()
        except:
            return False

    def _actually_load_lora(self, model, clip, lora_path, strength_model, strength_clip, flux_mode):
        """实际加载逻辑"""
        lora_data = load_torch_file(lora_path)
        
        if flux_mode:
            model.model.diffusion_model = model.model.diffusion_model.to(torch.float8_e4m3fn)

        if clip is None:
            model_lora, _ = load_lora_for_models(model, None, lora_data, strength_model, 0.0)
            return (model_lora, None)
        else:
            model_lora, clip_lora = load_lora_for_models(model, clip, lora_data, strength_model, strength_clip)
            return (model_lora, clip_lora)

    def generate_debug_report(self, path):
        """生成调试报告"""
        report = f"""
        === LoRA加载调试报告 ===
        路径: {path}
        存在: {os.path.exists(path)}
        大小: {os.path.getsize(path) if os.path.exists(path) else 0} bytes
        权限: {'可读' if os.access(path, os.R_OK) else '不可读'}
        类型: {'文件' if os.path.isfile(path) else '目录'}
        扩展名: {os.path.splitext(path)[1]}
        """
        print(report)

# 节点注册（关键修改部分）
NODE_CLASS_MAPPINGS = {"LoRALoader_path": LoRALoader_path} 
NODE_DISPLAY_NAME_MAPPINGS = {"LoRALoader_path": "PD_loraload_path"}