# pip install reportlab
import re
import random
import string
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体
pdfmetrics.registerFont(TTFont('SimHei', 'simhei.ttf'))  # 使用黑体字体

def generate_random_string(length=8):
    """生成指定长度的随机字符串"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def generate_timestamp_filename():
    """生成包含年月日时分秒和随机字符串的文件名"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    random_str = generate_random_string(8)
    return f"{timestamp}_{random_str}.pdf"

def create_grid_pdf(text, grid_size=1.57*cm, margin=1*cm, page_width=21*cm, page_height=29.7*cm, cols=12):
    # 生成包含日期和时间的文件名
    filename = generate_timestamp_filename()
    
    # 创建一个新的PDF文档
    c = canvas.Canvas('/var/www/html/defaultwww/tzg/pdfs/' + filename, pagesize=(page_width, page_height))
    
    # 获取页面宽度和高度
    width, height = page_width, page_height
    
    # 计算每行和每列的田字格数量
    rows = int((height - 2 * margin) // grid_size)
    
    # 设置字体大小
    font_size = 32  # 更改字体大小为32
    c.setFont("SimHei", font_size)  # 设置字体为黑体
    
    # 设置线条颜色为灰色
    line_color = (0.5, 0.5, 0.5)  # 灰色
    c.setStrokeColorRGB(*line_color)

    # 设置文本颜色为灰色
    text_color = (0.3, 0.3, 0.3)  # 灰色
    c.setFillColorRGB(*text_color)
    
    # 去掉空格和标点符号
    text = re.sub(r'[^\w]', '', text)
    
    # 将输入的文本拆分成字符列表
    characters = list(text)
    
    # 开始绘制田字格
    char_index = 0
    page_number = 1
    
    while char_index < len(characters):
        for row in range(rows):
            for col in range(cols):
                x = margin + col * grid_size
                y = height - (margin + (row + 1) * grid_size)
                
                # 绘制田字格的外框
                c.rect(x, y, grid_size, grid_size)
                
                # 绘制田字格的中间虚线
                c.setDash(2, 2)  # 设置虚线模式
                c.line(x, y + grid_size / 2, x + grid_size, y + grid_size / 2)
                c.line(x + grid_size / 2, y, x + grid_size / 2, y + grid_size)
                c.setDash()  # 恢复默认的实线模式
                
                # 在每行的第一个格子里写入指定的汉字
                if col == 0 and char_index < len(characters):
                    text = characters[char_index]
                    # 计算文本的位置，使其居中
                    text_width = c.stringWidth(text, "SimHei", font_size)
                    text_height = font_size  # 字体高度与字体大小相同
                    text_x = x + (grid_size - text_width) / 2
                    text_y = y + (grid_size - text_height) / 2 + (text_height / 3) - 5  # 调整垂直居中位置
                    c.drawString(text_x, text_y, text)
                    char_index += 1
            
            # 如果所有字符都已写完，则停止绘制
            if char_index >= len(characters):
                break
        
        # 如果当前页未写满所有字符，继续绘制下一页
        if char_index < len(characters):
            c.showPage()  # 换页
            page_number += 1
            c.setFont("SimHei", font_size)  # 重新设置字体
            c.setFillColorRGB(*text_color)  # 重新设置文本颜色
    
    # 如果最后一行没有写满字符，继续绘制剩余的田字格
    if char_index < len(characters) or (char_index % (cols * rows) != 0):
        for row in range(char_index // cols, rows):
            for col in range(cols):
                x = margin + col * grid_size
                y = height - (margin + (row + 1) * grid_size)
                
                # 绘制田字格的外框
                c.rect(x, y, grid_size, grid_size)
                
                # 绘制田字格的中间虚线
                c.setDash(2, 2)  # 设置虚线模式
                c.line(x, y + grid_size / 2, x + grid_size, y + grid_size / 2)
                c.line(x + grid_size / 2, y, x + grid_size / 2, y + grid_size)
                c.setDash()  # 恢复默认的实线模式
    
    # 保存PDF文档
    c.save()
    #print(f"PDF文件已保存为: {filename}")
    return filename

# 指定要写入的文字
#text = '年村这是一个示例文本用于展示如何将文字拆分成单个字符' * 10  # 重复文本以生成多页

# 创建PDF文件
#create_grid_pdf(text)
