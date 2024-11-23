import os
import uuid
from pdfrw import PdfReader, PdfWriter

class PdfExtractor:
    def __init__(self, input_pdf, save_directory):
        """
        初始化PdfExtractor实例。

        :param input_pdf: 输入的PDF文件路径
        :param save_directory: 保存提取页面的目录
        """
        self.input_pdf = input_pdf
        self.save_directory = save_directory
        self.reader = PdfReader(self.input_pdf)
        self.total_pages = len(self.reader.pages)

    def validate_pages(self, start_page, end_page):
        """
        验证提供的页码是否有效。

        :param start_page: 开始页码（包含）
        :param end_page: 结束页码（包含）
        :return: 如果页码有效返回True，否则抛出异常
        """
        if start_page < 1 or end_page > self.total_pages or start_page > end_page:
            raise ValueError('提供的页码无效，请检查页码范围')
        return True

    def extract_pages(self, start_page, end_page):
        """
        从PDF中提取指定范围的页面并保存为新的PDF文件。

        :param start_page: 开始页码（包含）
        :param end_page: 结束页码（包含）
        :return: 新PDF文件的路径
        """
        # 验证页码有效性
        self.validate_pages(start_page, end_page)
        
        # 创建一个新的PDF写入对象
        writer = PdfWriter()
        
        # 添加指定范围内的页面
        for page_num in range(start_page - 1, end_page):
            writer.addpage(self.reader.pages[page_num])
        
        # 生成唯一的输出文件名
        output_filename = f'{uuid.uuid4()}.pdf'
        output_path = os.path.join(self.save_directory, output_filename)
        
        # 确保保存目录存在
        os.makedirs(self.save_directory, exist_ok=True)
        
        # 将提取的页面写入新的PDF文件
        writer.write(output_path)
        
        return output_filename

# 使用示例
'''
input_pdf_path = 'example.pdf'  # 输入PDF文件路径
save_directory = 'extracted_pages'  # 保存提取页面的目录
extractor = PdfExtractor(input_pdf_path, save_directory)
start_page = 2  # 开始页码
end_page = 5  # 结束页码

output_pdf_path = extractor.extract_pages(start_page, end_page)
print(f'已创建新PDF文件：{output_pdf_path}')
'''
