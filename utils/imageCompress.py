from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def compress_image(image):
    img = Image.open(image)
    img = img.convert("RGB")  # تبدیل به RGB برای سازگاری

    max_size = (800, 800)  # تغییر اندازه به حداکثر 800x800 پیکسل
    img.thumbnail(max_size,Image.ANTIALIAS)  # thumbnail() تصویر را کوچک می‌کند ولی نسبت تصویر (aspect ratio) را حفظ می‌کند تا کشیدگی و تغییر شکل ایجاد نشود.
    # 🔸 Image.ANTIALIAS باعث افزایش کیفیت تصویر پس از کوچک شدن می‌شود.

    output = BytesIO()
    img.save(output, format="JPEG", quality=70)  # کاهش کیفیت به 70٪
    output.seek(0)

    compressed_image = InMemoryUploadedFile(
        output, "ImageField", image.name, "image/jpeg",
        sys.getsizeof(output), None
    )

    return compressed_image
