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
                        #entity.x = pygame.mouse.get_pos()[0]
                        #entity.y = pygame.mouse.get_pos()[1]
                        #print(entity)
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
    # init board tiles

    # init cards

    # scramble cards
    #init reactionlist
    #global REACTIONSET
    #preReactionSet = makeReactionSet(pathway_name='PWY-241')
    #REACTIONSET = preReactionSet[0]
    #REACTIONSET = makeReactionSet(pathway_name='PWY-241')
    #global SOURCE
    #SOURCE = preReactionSet[1][0]
    #global SINK
    #SINK = preReactionSet[1][-1]
    #global RUNNING
    global SCORE
    global RUNNING
    BOARD_X = 3
    BOARD_Y = 2
    entityList = []
    for  i in range(0,BOARD_X-1):
        for j in range(0, BOARD_Y):
            entityList.append(Card(length=50,pos_x=BOARD_X,pos_y=j))
    for e in entityList:
        e.filter_left.choose_color((255,255,255))
        print(e)
        e.filter_right.choose_color((255,255,255))
    #print(REACTIONSET)
    #appendSource(entityList)
    #appendSink(entityList,SINK)
    #entityList.append(Wall())
    #p = PreviewPanel()
    #PREVIEWPANEL = p
    #e, pp, r = makeEnzymesMetabolites(REACTIONSET[0])
    #p.nextEnzyme = e
    #entityList.append(p)
    #spawningTime = 0
    countdown_time = 9900
    time_played = 0
    while RUNNING:
        dt = clock.tick(60)
        #spawningTime += dt # new source metab every 0.8sec
        checkEvents(entityList)
        screen.fill((0, 0, 0))
        #todo
        if countdown_time > 0:
            addText(screen=screen, font=font, txt=countdown_time, pos=(WIDTH-400, 10))
            countdown_time -= dt
            time_played = 0
        else:
            time_played += dt
            RUNNING = False
            #addText(screen=screen, font=font, txt=time_played, pos=(WIDTH-200, 10))

        #if FLOW and spawningTime > 800:
        #    spawnSourceMetabolite(entityList,SOURCE)
        #    spawningTime = 0

        screen.blit(screen, (0, 0))
        for i, e in enumerate(entityList):
            # if isinstance(e, Enzyme):
            #     e.addText(screen=screen, font=enzyme_font)
            # elif isinstance(e, Metabolite):
            #     e.addText(screen=screen, font=metabolite_font)
            # elif isinstance(e,Sink):
            #     e.addText(screen=screen,font=score_font)
            # elif isinstance(e, PreviewPanel):
            #     e.addText(screen=screen, font=enzyme_font)
                #print(e.name)
            #if not e.textDrawn:
            #    e.addText(screen=screen, font=font)

            #e.checkCollisionList(entityList[:i],entityList=entityList)
            # bounceOff(e)
            # if isOutOfSight(e):
            #     entityList.remove(e)
            #     screen.blit(screen, (0, 0))
            # e.move()
            e.draw(screen)
            # if isinstance(e,Sink):
            #     pygame.draw.rect(screen, e.color, e.boundingbox, 2)

        pygame.display.flip()


# def bounceOff(entity):
#     if entity.x+entity.xsize > WIDTH or entity.x <0:
#         if entity.xvel > 0:
#             entity.xvel += 0
#         else:
#             entity.xvel -=0
#         entity.xvel *=-1
#         entity.move()
#
#     if entity.y+entity.ysize > HEIGHT or entity.y < 0:
#         if entity.yvel > 0:
#             entity.yvel += 0
#         else:
#             entity.yvel -= 0
#         entity.yvel *= -1
#         entity.move()

#
# def isOutOfSight(entity):
#     out = False
#     if entity.x > WIDTH or entity.x < 0 or entity.y > HEIGHT or entity.y < 0:
#         out = True
#     return out

# gets all species from elementtree list, return them sorted inversely by 'weights'
# def getSortedSp (species_list,weights):
#     #get all species from list
#     newSpList = []
#     for species in species_list:
#         for eachsp in species:
#             newSpList.append(eachsp.attrib['species'])
#     # pair with weight
#     sortedSp={}
#     for key in newSpList:
#         sortedSp[key] = weights[key]
#     # convert to list sorted by key
#     sortedSpList = sorted(sortedSp.iteritems(), key=operator.itemgetter(1))
#     # inverse
#     sortedSpList = sortedSpList[::-1]
#     # drop weight, leaving only ID
#     sortedSpList = [x[0] for x in sortedSpList]
#     return sortedSpList

# def makeReactionSet (xml='enzymes_out_curr.xml',weight_file='dummysize.txt',pathway_name=None):
#     all_reac_prod = {}
#     weights = {}
#     weightf = open(weight_file)
#     for line in weightf:
#         line = line.rstrip()
#         met = line.split('\t')[0] #todo with real input may or maynot need a replace command
#         w_met = float(line.split('\t') [1])
#         weights[met] = w_met
#     #print(weights)
#
#     pathwaytree = etree.parse(xml)
#     pathwaytree = pathwaytree.getroot()
#     """prepare new Reaction objects from XML"""
#     res = []
#     newres = []
#     longest_cycle = []
#     for pathway in pathwaytree.getiterator(tag='pathway'):
#         #read every pathway in file if un specified or read just specified pathway
#         if pathway_name is None or pathway.attrib['name'] == pathway_name:
#             for reaction in pathway:
#
#                 try:
#                     # get sorted reaction info
#                     newReactionName = reaction.attrib['name']
#                     newReactantList = getSortedSp(species_list=reaction.getiterator(tag='listOfReactants'),weights=weights)
#                     newProductList = getSortedSp(species_list=reaction.getiterator(tag='listOfProducts'),weights=weights)
#                     # append to list of reactions
#
#                     r = Reaction(name=newReactionName, enzymeName=newReactionName, listOfProducts=newProductList, listOfReactants=newReactantList, pathway=pathway.attrib['name'])
#                     res.append(r)
#
#                     num_pairs = min(len(newReactantList),len(newProductList))
#                     for i in range(0,num_pairs):
#                         all_reac_prod[newReactantList[i]] = newProductList[i]
#                     print (all_reac_prod)
#                 except Exception as e:
#                     print(e)
#
#             #find largest circles in pathway
#             remaining_reacs = list(all_reac_prod.keys())
#             cycles = []
#             i = 0
#             while(len(remaining_reacs) > 0):
#                 onemore = True
#                 start = remaining_reacs[0]
#                 remaining_reacs.pop(0)
#                 cycles.append([start])
#                 thenext = start
#                 while onemore:
#                     if thenext in all_reac_prod.keys():
#                         thenext = all_reac_prod[thenext]
#                         if thenext != start:
#                             cycles[i].append(thenext)
#                             if thenext in remaining_reacs:
#                                 remaining_reacs.remove(thenext)
#                         else:
#                             onemore = False
#                             cycles[i].append('cycle')
#                     else:
#                         onemore = False
#                 i +=1
#             cycles = [x[:-1] for x in cycles if x[-1] == 'cycle']
#             lengths_cycs = [len(x) for x in cycles]
#             longest_cycle = [cycles[i] for i in range(len(lengths_cycs)) if lengths_cycs[i] == max(lengths_cycs)]
#             if (len(longest_cycle) > 1):
#                 print "Warning, tie for longest cycle, using first"
#             longest_cycle = longest_cycle[0]
#             print(longest_cycle)
#             #sort the reaction pathway by the longest_cycle
#             for i in range(len(longest_cycle)):
#                 j = i + 1
#                 if j == len(longest_cycle):
#                     j = 0
#                 matching_rxn = []
#                 for rxn in res:
#                     if longest_cycle[i] in rxn.listOfReactants and longest_cycle[j] in rxn.listOfProducts:
#                         matching_rxn.append(rxn)
#                 if len(matching_rxn) == 1:
#                     newres.append(matching_rxn[0])
#                 else:
#                     print "Failed, unique and complete sort of input cycle elements. " + str(len(matching_rxn)) + " elements after " + longest_cycle[i] + ", 1 required"
#     return (newres,longest_cycle)


def addText(screen, font, txt, pos = (HEIGHT/2, WIDTH/3)):
        tmpfont = font.render(str(txt), True, (255, 255, 255))
        rect = tuple(tmpfont.get_rect())
        #print(rect)
        #tmpwidth = rect[2]
        #tmpheight = rect[3]
        #textxOffset += 0.02
        screen.blit(tmpfont, pos)
if __name__ == "__main__":
    main()
