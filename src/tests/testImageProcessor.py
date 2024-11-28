import pytest
import cv2
import numpy as np
from PIL import Image, ExifTags
from main import ImageProcessor  # 假设你的类保存为 image_processor.py

@pytest.fixture
def sample_image(tmp_path):
    """生成带有 EXIF Orientation 信息的测试图像"""
    image_path = tmp_path / "test_image.jpg"
    img = Image.new("RGB", (100, 100), color="red")
    
    # 添加 EXIF 信息
    exif_data = {
        ExifTags.TAGS_INV['Orientation']: 6  # 对应顺时针旋转90°
    }
    exif_bytes = piexif.dump({"0th": exif_data})
    img.save(image_path, exif=exif_bytes)
    return image_path

def test_correct_image_orientation(sample_image):
    """测试 correct_image_orientation 方法"""
    processor = ImageProcessor(sample_image)
    processor.correct_image_orientation()

    # 重新加载图片以验证
    corrected_image = cv2.imread(str(sample_image))
    expected_image = np.zeros((100, 100, 3), dtype=np.uint8)
    expected_image[:] = [0, 0, 255]  # Red in BGR format

    # 比较像素值
    assert corrected_image.shape == (100, 100, 3)
    assert np.array_equal(corrected_image, expected_image), "Image orientation correction failed."
