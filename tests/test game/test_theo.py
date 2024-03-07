import pygame.font

pygame.font.init()

# Obtenez la liste des polices disponibles
available_fonts = pygame.font.get_fonts()

# Affichez la liste des polices
for font_name in available_fonts:
    print(font_name)
