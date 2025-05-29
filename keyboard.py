import pygame
import time
pygame.init()

# Screen settings
def keyboard(blink_queue):
    WIDTH, HEIGHT = 800, 300
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Keyboard")
    WHITE = (255, 255, 255)
    GRAY = (180, 180, 180)
    BLUE = (100, 100, 255)
    BLACK = (0, 0, 0)

    font = pygame.font.Font(None, 36)
    count =0

    key_width = 60
    key_height = 60
    key_margin = 10
    start_x = 50
    start_y = 50

    keys = [
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
    ] 

    blink_index = 0
    blink_time = 800  # ms
    last_blink = pygame.time.get_ticks()
    print ("las",last_blink)

    running = True
    while running:
        screen.fill(WHITE)

        # Draw keys
        key_rects = []
        for row_index, row in enumerate(keys):
            for col_index, key in enumerate(row):
                x = start_x + col_index * (key_width + key_margin)
                y = start_y + row_index * (key_height + key_margin)
                rect = pygame.Rect(x, y, key_width, key_height)
                if count == blink_index:
                    Letter = key
                    pygame.draw.rect(screen, BLUE, rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                text = font.render(key, True, BLACK)
                count=count+1
                
                screen.blit(text, (x + 20, y + 15))
                key_rects.append((rect, key))
        count=0
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, key in key_rects:
                    if rect.collidepoint(pos):
                        print(f"Key pressed: {key}")

        current_time = pygame.time.get_ticks()
        if current_time - last_blink > blink_time:
            blink_index = (blink_index + 1) % 26
            last_blink = current_time

        if not blink_queue.empty():
            msg = blink_queue.get()
            if msg == "BLINK":
                selected_key = Letter
                print(selected_key,end="")    
                time.sleep(1)
        pygame.display.flip()

    pygame.quit()