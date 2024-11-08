from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re
import random
import string
from datetime import datetime

class GridPDFCreator:
    def __init__(self, entries, grid_size=1.57*cm, margin=1*cm, page_width=21*cm, page_height=29.7*cm, cols=12):
        self.entries = entries
        self.grid_size = grid_size
        self.margin = margin
        self.page_width = page_width
        self.page_height = page_height
        self.cols = cols
        self.rows = int((page_height - 2 * margin) // grid_size)
        self.filename = self.generate_timestamp_filename()
        self.c = canvas.Canvas('/var/www/html/defaultwww/tzg/pdfs/' + self.filename, pagesize=(page_width, page_height))
        #self.c = canvas.Canvas(self.filename, pagesize=(page_width, page_height))
        self.top_text_font_size = 14
        self.grid_text_font_size = 32
        # 注册中文字体
        font_path_simhei = 'simhei.ttf'
        font_path_simsun = 'simsun.ttf'
        pdfmetrics.registerFont(TTFont('SimHei', font_path_simhei))
        pdfmetrics.registerFont(TTFont('SimSun', font_path_simsun))

    def generate_timestamp_filename(self):
        """生成包含年月日时分秒和随机字符串的文件名"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_str = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{timestamp}_{random_str}.pdf"

    def draw_centered_text(self, text, y_position=None):
        """输出居中的字符串并返回最后的坐标"""
        c = self.c
        top_text_width = c.stringWidth(text, "SimSun", self.top_text_font_size)
        top_text_x = (self.page_width - top_text_width) / 2
        if y_position is None:
            top_text_y = self.page_height - self.margin - self.top_text_font_size
        else:
            top_text_y = y_position - self.margin - self.top_text_font_size
        c.setFont("SimSun", self.top_text_font_size)
        c.drawString(top_text_x, top_text_y, text)
        return top_text_y

    def draw_grid(self, characters, start_y, char_index=0):
        """输出田字格并返回最后的坐标"""
        c = self.c
        current_y = start_y
        
        while char_index < len(characters):
            for col in range(self.cols):
                x = self.margin + col * self.grid_size
                y = current_y - (self.grid_size)
                
                # 检查是否需要换页
                if y < self.margin:
                    c.showPage()  # 换页
                    current_y = self.page_height - self.margin + self.grid_size
                    break
                
                # 绘制田字格的外框
                c.setStrokeColorRGB(0.5, 0.5, 0.5)
                c.rect(x, y, self.grid_size, self.grid_size)
                
                # 绘制田字格的中间虚线
                c.setDash(2, 2)  # 设置虚线模式
                c.line(x, y + self.grid_size / 2, x + self.grid_size, y + self.grid_size / 2)
                c.line(x + self.grid_size / 2, y, x + self.grid_size / 2, y + self.grid_size)
                c.setDash()  # 恢复默认的实线模式
                
                # 在每行的第一个格子里写入指定的汉字
                if col == 0 and char_index < len(characters):
                    text = characters[char_index]
                    # 计算文本的位置，使其居中
                    c.setFont("SimHei", self.grid_text_font_size)  # 设置字体为黑体
                    text_width = c.stringWidth(text, "SimHei", self.grid_text_font_size)
                    text_height = self.grid_text_font_size  # 字体高度与字体大小相同
                    text_x = x + (self.grid_size - text_width) / 2
                    text_y = y + (self.grid_size - text_height) / 2 + (text_height / 3) - 5  # 调整垂直居中位置
                    c.drawString(text_x, text_y, text)
                    char_index += 1
            
            # 如果已经绘制完所有字符，跳出循环
            if char_index >= len(characters):
                break
            
            # 移动到下一行
            current_y -= self.grid_size

        current_y -= self.grid_text_font_size
        return current_y, char_index

    def create_pdf(self):
        """创建PDF文件"""
        current_start_y = None
        current_entry_index = 0
        
        while current_entry_index < len(self.entries):
            top_text, grid_text = self.entries[current_entry_index]
            grid_text = re.sub(r'[^\w]', '', grid_text)
            characters = list(grid_text)
            
            # 绘制顶部居中的文字
            top_text_y = self.draw_centered_text(top_text, current_start_y)
            
            # 使用新增的间距参数
            current_start_y, char_index = self.draw_grid(characters, top_text_y - self.margin + self.top_text_font_size)
            
            # 如果所有字符都已绘制完毕，移动到下一个条目
            if char_index >= len(characters):
                current_entry_index += 1
        
        self.c.save()
        #print(f"PDF 文件已创建：{self.filename}")
        return self.filename

# 修改后的示例数据，使用二维列表代替字典
'''
entries = [
    ['1、小蝌蚪找妈妈', '两哪宽顶眼睛肚皮孩跳'],
    ['2、我是什么', '变机片傍海洋作坏给带'],
    ['3、植物妈妈有办法', '法如公它娃她毛更知识'],
    ['4、小蝌蚪找妈妈', '两哪宽顶眼睛肚皮孩跳'],
    ['5、我是什么', '变机片傍海洋作坏给带'],
    ['6、植物妈妈有办法', '法如公它娃她毛更知识'],
    ['7、植物妈妈有办法', '法如公它娃她毛更知识']
]
'''
# 创建PDF文件
'''
pdf_creator = GridPDFCreator(entries)
fname = pdf_creator.create_pdf()
print(fname)
'''
