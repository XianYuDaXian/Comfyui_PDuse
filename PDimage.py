import torch
from torchvision import transforms
from PIL import Image
import numpy as np

def pil2tensor(image):
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class PD_Image_Crop_Location:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),  # 输入图像张量 [B, H, W, C]
                "x": ("INT", {"default": 0, "min": 0, "max": 10000000, "step": 1}),  # 裁剪区域左上角 X 坐标
                "y": ("INT", {"default": 0, "min": 0, "max": 10000000, "step": 1}),  # 裁剪区域左上角 Y 坐标
                "width": ("INT", {"default": 256, "min": 1, "max": 10000000, "step": 1}),  # 裁剪区域宽度
                "height": ("INT", {"default": 256, "min": 1, "max": 10000000, "step": 1}),  # 裁剪区域高度
            }
        }

    RETURN_TYPES = ("IMAGE",)  # 返回裁切后的图像张量
    RETURN_NAMES = ("Result",)  # 返回值的名称
    FUNCTION = "image_crop_location"  # 指定执行的方法名称
    CATEGORY = "PD_Image/Process"  # 定义节点的类别

    def image_crop_location(self, image, x=0, y=0, width=256, height=256):
        """
        通过给定的 x, y 坐标和裁切的宽度、高度裁剪图像。

        参数：
            image (tensor): 输入图像张量 [B, H, W, C]
            x (int): 裁剪区域左上角 X 坐标
            y (int): 裁剪区域左上角 Y 坐标
            width (int): 裁剪区域宽度
            height (int): 裁剪区域高度

        返回：
            (tensor): 裁剪后的图像张量 [B, H', W', C]
        """
        # 确保输入图像张量的格式正确 [B, H, W, C]
        if image.dim() != 4:
            raise ValueError("输入图像张量必须是 4 维的 [B, H, W, C]")

        # 获取输入图像的尺寸
        batch_size, img_height, img_width, channels = image.shape

        # 检查裁剪区域是否超出图像范围
        if x >= img_width or y >= img_height:
            raise ValueError("裁剪区域超出图像范围")

        # 计算裁剪区域的右下边界坐标
        crop_left = max(x, 0)
        crop_top = max(y, 0)
        crop_right = min(crop_left + width, img_width)
        crop_bottom = min(crop_top + height, img_height)

        # 确保裁剪区域的宽度和高度大于零
        crop_width = crop_right - crop_left
        crop_height = crop_bottom - crop_top
        if crop_width <= 0 or crop_height <= 0:
            raise ValueError("裁剪区域无效，请检查 x, y, width 和 height 的值")

        # 裁剪图像张量
        cropped_image = image[:, crop_top:crop_bottom, crop_left:crop_right, :]

        # 调整裁剪后的图像尺寸为 8 的倍数（可选）
        new_height = (cropped_image.shape[1] // 8) * 8
        new_width = (cropped_image.shape[2] // 8) * 8
        if new_height != cropped_image.shape[1] or new_width != cropped_image.shape[2]:
            cropped_image = torch.nn.functional.interpolate(
                cropped_image.permute(0, 3, 1, 2),  # [B, C, H, W]
                size=(new_height, new_width),
                mode="bilinear",
                align_corners=False,
            ).permute(0, 2, 3, 1)  # [B, H, W, C]

        return (cropped_image,)

class PD_Image_centerCrop:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),  # 输入图像张量 [B, H, W, C]
                "W": ("INT", {"default": 0, "min": 0, "max": 10000000, "step": 1}),  # 左右两边各自裁切的宽度
                "H": ("INT", {"default": 0, "min": 0, "max": 10000000, "step": 1}),  # 上下两边各自裁切的高度
            }
        }

    RETURN_TYPES = ("IMAGE",)  # 返回裁切后的图像张量
    RETURN_NAMES = ("Result",)  # 返回值的名称
    FUNCTION = "center_crop"  # 指定执行的方法名称
    CATEGORY = "PD_Image/Process"  # 定义节点的类别

    def center_crop(self, image, W, H):
        """
        根据动态输入的 W 和 H 值，在左右和上下两边等边裁切，确保裁切后的图像居中。

        参数：
            image (tensor): 输入图像张量 [B, H, W, C]
            W (int): 动态输入的 W 值（左右两边各自裁切的宽度）
            H (int): 动态输入的 H 值（上下两边各自裁切的高度）

        返回：
            (tensor): 裁切后的图像张量 [B, H', W', C]
        """
        # 确保输入图像张量的格式正确 [B, H, W, C]
        if image.dim() != 4:
            raise ValueError("输入图像张量必须是 4 维的 [B, H, W, C]")

        # 获取输入图像的尺寸
        batch_size, img_height, img_width, channels = image.shape

        # 检查 W 和 H 是否有效
        if W < 0 or W >= img_width / 2:
            raise ValueError(f"W 的值无效，必须满足 0 <= W < {img_width / 2}")
        if H < 0 or H >= img_height / 2:
            raise ValueError(f"H 的值无效，必须满足 0 <= H < {img_height / 2}")

        # 计算左右裁切的起始点 x 和裁切宽度 width
        x = W
        width = img_width - 2 * W

        # 计算上下裁切的起始点 y 和裁切高度 height
        y = H
        height = img_height - 2 * H

        # 裁剪图像张量
        cropped_image = image[:, y:y + height, x:x + width, :]

        return (cropped_image,)

class PD_GetImageSize:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("INT", "INT")  # 输出宽高
    RETURN_NAMES = ("width", "height")
    FUNCTION = "get_size"
    CATEGORY = "Masquerade Nodes"
    OUTPUT_NODE = True  # 启用输出节点功能

    def get_size(self, image, unique_id=None, extra_pnginfo=None):
        # 检查 image 是否为 None
        if image is None:
            raise ValueError("No image provided to PD:GetImageSize node")

        # 获取宽高信息
        image_size = image.size()
        image_width = int(image_size[2])
        image_height = int(image_size[1])

        # 将宽高信息转换为字符串
        size_info = f"Width: {image_width}, Height: {image_height}"

        # 更新节点界面显示
        if extra_pnginfo and isinstance(extra_pnginfo, list) and "workflow" in extra_pnginfo[0]:
            workflow = extra_pnginfo[0]["workflow"]
            node = next((x for x in workflow["nodes"] if str(x["id"]) == unique_id), None)
            if node:
                node["widgets_values"] = [size_info]  # 将宽高信息显示在节点界面上

        # 返回宽高信息
        return (image_width, image_height, {"ui": {"text": [size_info]}})
    
import os
import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class ImageMergerWithText:
    """
    一个将两张图片左右合并并在下方添加文字说明的节点
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        # 获取当前脚本所在目录的 fonts 子目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        fonts_dir = os.path.join(current_dir, "fonts")
        
        # 扫描 fonts 目录下的所有 .ttf 和 .otf 文件
        font_files = []
        if os.path.exists(fonts_dir):
            font_files = [
                f for f in os.listdir(fonts_dir)
                if f.lower().endswith(('.ttf', '.otf'))
            ]
        
        # 如果没有找到字体文件，则默认使用系统字体
        if not font_files:
            font_files = ["system"]  # 默认选项
        
        return {
            "required": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "text1": ("STRING", {"default": "Image 1"}),
                "text2": ("STRING", {"default": "Image 2"}),
                "font_size": ("INT", {"default": 30, "min": 10, "max": 100, "step": 1}),
                "padding_up": ("INT", {"default": 20, "min": 0, "max": 100, "step": 1}),
                "padding_down": ("INT", {"default": 20, "min": 0, "max": 1000, "step": 1}),
                "font_file": (font_files, {"default": font_files[0]}),  # 显示所有字体文件供选择
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "merge_images"
    CATEGORY = "image/processing"

    def merge_images(self, image1, image2, text1, text2, font_size=30, padding_up=20, padding_down=20, font_file="system"):
        # 转换张量为PIL图像
        img1 = self._safe_tensor_to_pil(image1)
        img2 = self._safe_tensor_to_pil(image2)
        
        # 计算缩放比例（以最长边为准）
        max_dimension = max(img1.width, img1.height, img2.width, img2.height)
        
        # 等比例缩放两张图片
        def resize_image(img):
            ratio = max_dimension / max(img.width, img.height)
            new_width = int(img.width * ratio)
            new_height = int(img.height * ratio)
            return img.resize((new_width, new_height), Image.LANCZOS)
        
        img1 = resize_image(img1)
        img2 = resize_image(img2)
        
        # 合并图片
        merged_img = Image.new("RGB", (img1.width + img2.width, max(img1.height, img2.height)))
        merged_img.paste(img1, (0, (merged_img.height - img1.height) // 2))  # 垂直居中
        merged_img.paste(img2, (img1.width, (merged_img.height - img2.height) // 2))  # 垂直居中
        
        # 加载字体
        font = self._load_font(font_size, font_file)
        
        # 计算文本尺寸（兼容新旧Pillow版本）
        try:
            # Pillow 10.0.0+ 使用新的textlength和textbbox方法
            text1_width = font.getlength(text1)
            text2_width = font.getlength(text2)
            _, _, _, text_height = font.getbbox("Ag")  # 使用包含下行字母的文本测量高度
        except AttributeError:
            # 旧版Pillow使用getsize方法
            text1_width, text_height = font.getsize(text1)
            text2_width, _ = font.getsize(text2)
        
        # 创建最终图像（带文字区域）
        bg_height = text_height + padding_up + padding_down
        final_img = Image.new("RGB", (merged_img.width, merged_img.height + bg_height), "black")
        final_img.paste(merged_img, (0, 0))
        
        # 绘制文字
        draw = ImageDraw.Draw(final_img)
        text_y = merged_img.height + padding_up
        
        # 第一张图的文字居中
        text1_x = img1.width // 2 - text1_width // 2
        draw.text((text1_x, text_y), text1, font=font, fill="white")
        
        # 第二张图的文字居中
        text2_x = img1.width + img2.width // 2 - text2_width // 2
        draw.text((text2_x, text_y), text2, font=font, fill="white")
        
        # 转换回张量
        return (self._pil_to_tensor(final_img),)
    
    def _safe_tensor_to_pil(self, tensor):
        """安全地将张量转换为PIL图像"""
        tensor = tensor.cpu().detach()
        
        # 处理批次维度
        if tensor.dim() == 4:
            tensor = tensor[0]
        
        # 处理通道顺序
        if tensor.shape[0] <= 4:  # CHW格式
            tensor = tensor.permute(1, 2, 0)
        
        # 归一化处理
        if tensor.dtype == torch.float32 and tensor.max() <= 1.0:
            tensor = tensor * 255
        
        # 转换为uint8
        tensor = tensor.to(torch.uint8)
        
        # 处理单通道图像
        if tensor.dim() == 2 or tensor.shape[-1] == 1:
            tensor = tensor.unsqueeze(-1) if tensor.dim() == 2 else tensor
            tensor = torch.cat([tensor]*3, dim=-1)  # 转为RGB
        
        return Image.fromarray(tensor.numpy())
    
    def _load_font(self, font_size, font_file="system"):
        """加载字体，优先从 fonts 目录加载"""
        if font_file == "system":
            try:
                return ImageFont.truetype("arial.ttf", font_size)
            except:
                return ImageFont.load_default()
        else:
            # 从插件目录的 fonts 子目录加载字体
            current_dir = os.path.dirname(os.path.abspath(__file__))
            font_path = os.path.join(current_dir, "fonts", font_file)
            try:
                return ImageFont.truetype(font_path, font_size)
            except Exception as e:
                print(f"⚠️ 字体加载失败: {font_file}, 回退到系统默认字体。错误: {e}")
                return ImageFont.load_default()
    
    def _pil_to_tensor(self, image):
        """将PIL图像转换为张量"""
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

# 在 ComfyUI 中的节点映射配置
NODE_CLASS_MAPPINGS = {
    "PD_Image_Crop_Location": PD_Image_Crop_Location,
    "PD_Image_centerCrop": PD_Image_centerCrop,
    "PD_GetImageSize": PD_GetImageSize, 
    "PD_ImageMergerWithText": ImageMergerWithText,   # 这个节点对应的类
    
}

# 设置节点在 UI 中显示的名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "PD_Image_Crop_Location": "PD:Image Crop Location",
    "PD_Image_centerCrop": "PD:Image centerCrop",
    "PD_GetImageSize": "PD:GetImageSize", 
    "ImageMergerWithText": "Image Merger With Text",  # 更新显示名称
}
