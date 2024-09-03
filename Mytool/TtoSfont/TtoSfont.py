# 让简体字采用繁体字形

import fontforge
import json

# 读取mapping.json文件
with open('mapping.json', 'r', encoding='utf-8') as file:
    mapping = json.load(file)

font = fontforge.open("chongxi-seal.ttf")  # 替换为你的字体文件路径

# 遍历mapping字典，直接将繁体字的轮廓导入到简体字的位置
for simp, trad in mapping.items():
    simp_unicode = ord(simp)
    trad_unicode = ord(trad)
    
    if trad_unicode in font:
        glyph = font[trad_unicode]
        font.selection.select(trad_unicode)
        font.copy()
        
        if simp_unicode not in font:
            empty_glyph = font.createChar(simp_unicode)
        font.selection.select(simp_unicode)
        font.paste()
    
# 保存修改后的字体文件
font.generate('output_font.ttf')  # 保存为新的字体文件

print("字体转换完成！")