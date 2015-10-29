import pygame
from color_puzzle_classes import Tile, Filter, Card

WIDTH = 800
HEIGHT = 600
SCORE = ""
##############
RUNNING = True
ACTIVE = None #selected Drawable

def checkEvents(entityList):
    global RUNNING
    global ACTIVE
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("escape")
                RUNNING = False
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.key == pygame.K_s:
                mouseX, mouseY = pygame.mouse.get_pos()
                pygame.display.toggle_fullscreen()

        if event.type == pygame.QUIT:
            RUNNING = False

        if event.type == pygame.MOUSEBUTTONDOWN: #select card
            if event.button:
                print("POS", event.pos)
                # clicked and moving
                rel = event.pos
                cardList = [e for e in entityList if isinstance(e, Card)]
                for entity in cardList:
                    if entity.shape.collidepoint(pygame.mouse.get_pos()):
                        print("entity", entity.id)
                        ACTIVE = entity.id
                        print(ACTIVE)
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            ACTIVE = None
        if event.type == pygame.MOUSEMOTION:
            #print(active_entity)
            try:
                if ACTIVE:
                    act = [e for e in entityList if isinstance(e, Card) and e.id == ACTIVE]
                    #print(act)
                    act[0].x = pygame.mouse.get_pos()[0]
                    act[0].y = pygame.mouse.get_pos()[1]
                    act[0].move_components()
                    #if event.button
                    #active_entity = None
            except UnboundLocalError:
                ACTIVE = None


# display score
def texts(screen, font):
    if not font:
        font=pygame.font.Font(None,42)
    scoretext=font.render(""+str(SCORE), 1,(99,99,88))
    screen.blit(scoretext, (500, 457))


def get_overlap(pos_x, pos_y, cards):
    out = Filter(1,0,0)
    if False:
        pass
    else:
#        print('card overlap')
        for card in cards:
            if card.filter_right.pos_x == pos_x and card.pos_y == pos_y:
                out = card.filter_right

    return out


def main():
    # global PREVIEWPANEL
    pygame.init()
    #todo
    font = pygame.font.Font("Arcade.ttf", 128)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("0h")
    pygame.mouse.set_visible(1)
    clock = pygame.time.Clock()
    # init

    global SCORE
    global RUNNING
    BOARD_X = 4
    BOARD_Y = 2
    entityList = []
    filterList = []
    for  i in range(0,BOARD_X-1):
        for j in range(0, BOARD_Y):
            entityList.append(Card(length=50,pos_x=i,pos_y=j))
    for e in entityList:
        left_other = get_overlap(e.pos_x, e.pos_y, entityList)
        e.filter_left.color = e.filter_left.calculate_color((255,255,255),left_other)
        e.filter_left.ori_color = e.filter_left.color
        e.filter_right.color = e.filter_right.choose_color((255,255,255))
        e.filter_right.ori_color = e.filter_right.color
        filterList.append(e.filter_right)
        filterList.append(e.filter_left)

    countdown_time = 99900
    time_played = 0
    while RUNNING:
        dt = clock.tick(60)
        checkEvents(entityList)
        for card in entityList:
            card.filter_left.checkCollisionList(filterList, ignore=card.filter_right)
            card.filter_right.checkCollisionList(filterList, ignore=card.filter_left)
        screen.fill((0, 0, 0))
        #todo
        if countdown_time > 0:
            addText(screen=screen, font=font, txt=countdown_time, pos=(WIDTH-400, 10))
            countdown_time -= dt
            time_played = 0
        else:
            time_played += dt
            RUNNING = False

        screen.blit(screen, (0, 0))
        for i, e in enumerate(entityList):
            e.draw(screen)

        pygame.display.flip()


def addText(screen, font, txt, pos = (HEIGHT/2, WIDTH/3)):
        tmpfont = font.render(str(txt), True, (255, 255, 255))
        rect = tuple(tmpfont.get_rect())
        screen.blit(tmpfont, pos)
if __name__ == "__main__":
    main()
