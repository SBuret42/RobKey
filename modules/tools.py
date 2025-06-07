#import st7789
#import math

"""
Tentative non fructueuse

def drawParagraphe(display, vector_font, s, x, y, fg=st7789.WHITE, taille=1.0): #Ecris un texte avec retour à la ligne automatique
    len_pixel_txt = display.draw_len(vector_font, s, taille)
    print(len_pixel_txt)
    print(math.ceil(len_pixel_txt)/170)
    display.init()
    for line in range(1,math.ceil(len_pixel_txt)/170):
        display.draw(vector_font, s, taille*line+x, taille*line+y + taille*10//2, fg, taille)
    display.deinit()

import romanp as font
drawParagraphe(display, font,"a",0,0)
drawParagraphe(display, font,"a",0,50, taille=2)
drawParagraphe(display, font,"aaaaaa",0,100, taille=3)
"""
    