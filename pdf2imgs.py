# pip install pymupdf
# pdf转图片
import fitz  # PyMuPDF
import os
import zipfile  # 导入zipfile模块
import uuid  # 导入uuid模块

class PdfToImagesConverter:
    def __init__(self, pdf_path, output_folder='./', zoom_x=1.0, zoom_y=1.0):
        self.pdf_path = pdf_path
        self.output_folder = output_folder
        self.zoom_x = zoom_x
        self.zoom_y = zoom_y
        self.pdf_document = None
        self.images_list = []
        self.zip_file_name = None

    def _ensure_output_folder_exists(self):
        """确保输出文件夹存在"""
        os.makedirs(self.output_folder, exist_ok=True)

    def _create_zip_file(self):
        """创建ZIP文件并将所有图片添加进去，然后删除原始图片"""
        self.zip_file_name = os.path.join(self.output_folder, f"{str(uuid.uuid4())}.zip")
        with zipfile.ZipFile(self.zip_file_name, 'w') as image_zip:
            for img in self.images_list:
                # 将每个图片写入ZIP文件，使用arcname参数避免复制整个路径
                image_zip.write(img, arcname=os.path.basename(img))
        
        #print(f'All images have been zipped into {self.zip_file_name}')
        
        # 删除原始图片
        for img in self.images_list:
            try:
                os.remove(img)
                #print(f'Deleted {img}')
            except OSError as e:
                print(f"Error: {img} could not be deleted - {e}")

    def convert_pdf_to_images(self, rotateDu=0):
        """将PDF转换为一系列图像，并保存到指定文件夹中"""
        if not os.path.isfile(self.pdf_path):
            raise FileNotFoundError(f"The file {self.pdf_path} does not exist.")
        
        self.pdf_document = fitz.open(self.pdf_path)
        self._ensure_output_folder_exists()

        # 遍历每一页
        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document.load_page(page_num)  # 加载页
            # 设置缩放和旋转系数
            trans = fitz.Matrix(self.zoom_x, self.zoom_y).prerotate(rotateDu)  # 注意这里使用的是 prerotate
            # 渲染图像
            pix = page.get_pixmap(matrix=trans)
            # 构造输出图片路径
            output_image = os.path.join(self.output_folder, f"page_{page_num + 1}.jpg")
            # 保存图片
            pix.save(output_image)
            #print(f'Saved {output_image}')
            self.images_list.append(output_image)  # 添加图片路径到列表
        
        self._create_zip_file()
        return self.zip_file_name  # 返回ZIP文件名

# 使用类进行PDF转换和压缩，并获取压缩包的名字
'''
converter = PdfToImagesConverter('a3.pdf')
zip_filename = converter.convert_pdf_to_images(rotateDu)
print(f'The generated ZIP file name is: {zip_filename}')
'''
