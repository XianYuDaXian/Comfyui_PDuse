import torch
from PIL import Image
import numpy as np
import os

# 假设 tensor2pil 和 pil2tensor 是已经存在的图像转换函数
def tensor2pil(tensor):
    return Image.fromarray(tensor.numpy())

def pil2tensor(pil_image):
    return torch.from_numpy(np.array(pil_image))

class PD_Image_Crop_Location:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {   # 定义必要的输入参数
                "image": ("IMAGE",),  # 输入的图像
                "x": ("INT", {"default": 0, "min": 0, "max": 10000000, "step": 1}),  # 裁剪区域左上角 X 坐标
                "y": ("INT", {"default": 0, "min": 0, "max": 10000000, "step": 1}),  # 裁剪区域左上角 Y 坐标
                "width": ("INT", {"default": 256, "min": 0, "max": 10000000, "step": 1}),  # 裁剪区域宽度
                "height": ("INT", {"default": 256, "min": 0, "max": 10000000, "step": 1}),  # 裁剪区域高度
            }
        }

    @classmethod
    def RETURN_TYPES(cls):
        return ["IMAGE", "CROP_DATA"]  # 这是返回列表的方式，正确

    @classmethod
    def FUNCTION(cls):
        return "image_crop_location"  # 函数名

    @classmethod
    def CATEGORY(cls):
        return "PD Suite/Image/Process"  # 分类

    def image_crop_location(self, image, x=0, y=0, width=256, height=256):
        # 将图像从 tensor 转换为 PIL 图像
        image = tensor2pil(image)

        # 获取图像的宽度和高度
        img_width, img_height = image.size

        # 计算裁剪区域的边界坐标
        crop_left = max(x, 0)
        crop_top = max(y, 0)
        crop_right = min(crop_left + width, img_width)
        crop_bottom = min(crop_top + height, img_height)

        # 确保裁剪区域的宽度和高度大于零
        crop_width = crop_right - crop_left
        crop_height = crop_bottom - crop_top
        if crop_width <= 0 or crop_height <= 0:
            raise ValueError("Invalid crop dimensions. Please check the values for x, y, width, and height.")

        # 执行裁剪操作
        crop = image.crop((crop_left, crop_top, crop_right, crop_bottom))

        # 返回裁剪后的图像和裁剪数据
        crop_data = (crop.size, (crop_left, crop_top, crop_right, crop_bottom))

        # 将裁剪后的图像调整为 8 的倍数
        crop = crop.resize((((crop.size[0] // 8) * 8), ((crop.size[1] // 8) * 8)))

        return (pil2tensor(crop), crop_data)

# 在 ComfyUI 的节点映射配置
NODE_CLASS_MAPPINGS = {
    "PD_Image_Crop_Location": PD_Image_Crop_Location,
}
#在 UI 中设置显示名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "PD_Image_Crop_Location": "PD Image Crop Location", 
}