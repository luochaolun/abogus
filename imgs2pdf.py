# pip install pillow reportlab
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

class ImageToPDFConverter:
    def __init__(self, image_folder, output_pdf):
        self.image_folder = image_folder
        self.output_pdf = output_pdf
        self.width, self.height = A4  # A4纸的宽度和高度
    
    def get_images(self):
        """获取文件夹中所有支持的图片文件"""
        return [img for img in os.listdir(self.image_folder) if img.endswith((".png", ".jpg", ".jpeg"))]

    def create_pdf(self):
        """创建PDF文档并添加图片"""
        c = canvas.Canvas(self.output_pdf, pagesize=A4)
        
        for image_file in self.get_images():
            full_path = os.path.join(self.image_folder, image_file)
            self.add_image_to_pdf(c, full_path)
        
        c.save()
    
    def add_image_to_pdf(self, canvas, image_path):
        """向PDF中添加单个图片"""
        with Image.open(image_path) as img:
            # 调整图片大小以适应A4页面
            img = img.resize((int(self.width), int(self.height)), Image.Resampling.LANCZOS)
            
            # 在PDF中添加图片
            canvas.drawImage(image_path, 0, 0, width=self.width, height=self.height)
            canvas.showPage()  # 新建一页

    def delete_images(self):
        """删除文件夹中的所有图片文件"""
        for image_file in self.get_images():
            full_path = os.path.join(self.image_folder, image_file)
            try:
                os.remove(full_path)
                print(f"Deleted: {full_path}")
            except Exception as e:
                print(f"Error deleting {full_path}: {e}")
'''
if __name__ == "__main__":
    # 指定图片文件夹路径和输出PDF文件名
    image_folder = './'  # 替换为你的图片文件夹路径
    output_pdf = 'output.pdf'  # 输出的PDF文件名
    
    converter = ImageToPDFConverter(image_folder, output_pdf)
    converter.create_pdf()
    #converter.delete_images()
'''
