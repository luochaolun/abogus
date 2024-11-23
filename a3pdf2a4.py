# pip install reportlab pdfrw
from reportlab.lib.pagesizes import A3, A4
from pdfrw import PdfReader, PdfWriter, PageMerge

class PDFSplitter:
    def __init__(self, input_pdf_path, output_pdf_path):
        self.input_pdf_path = input_pdf_path
        self.output_pdf_path = output_pdf_path
        self.reader = PdfReader(self.input_pdf_path)
        self.writer = PdfWriter()

    def is_a3_page(self, page):
        """ 检查给定的页面是否为A3大小 """
        width, height = float(page.MediaBox[2]), float(page.MediaBox[3])
        a3_width, a3_height = A3
        return abs(width - a3_width) < 1 and abs(height - a3_height) < 1

    def split_a3_to_a4(self):
        """ 如果页面是A3，则将其分割为两个A4页面 """
        for page in self.reader.pages:
            '''
            if not self.is_a3_page(page):
                print(f"警告：页面不是A3大小，跳过此页面。")
                continue
            '''
            # 获取页面的尺寸
            a3_width, a3_height = A3
            a4_width = a3_width / 2
            _, a4_height = A4

            # 计算裁剪区域
            left_rect = (0, 0, a4_width, a4_height)  # 左半部分
            right_rect = (a4_width, 0, a4_width, a4_height)  # 右半部分

            # 将A3页面分为两个A4页面
            left_page = PageMerge().add(page, viewrect=left_rect).render()
            right_page = PageMerge().add(page, viewrect=right_rect).render()

            # 添加到输出PDF中
            self.writer.addpage(left_page)
            self.writer.addpage(right_page)

        # 写入到新的PDF文件
        self.writer.write(self.output_pdf_path)

# 使用类
'''
if __name__ == "__main__":
    splitter = PDFSplitter('a3.pdf', 'a4.pdf')
    splitter.split_a3_to_a4()
'''
