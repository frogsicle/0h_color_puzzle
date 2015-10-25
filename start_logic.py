
def initiate():

    def get_overlap(pos_x, pos_y, cards, filters_left, filters_right, boardY):
        if pos_y == 0:
            for item in filters_left:
                if item.pos_x == pos_x:
                    return item
        elif pos_y == boardY:
            for item in filters_right:
                if item.pos_x == pos_x:
                    return item
        else:
            for card in cards:
                if card.pos_x == pos_x & card.pos_y == pos_y:
                    return card

    col_target = (255,255,255)
    boardX = 3
    boardY = 2
    n_col = 2
    length = 50
    cards = []
    filters_left = []
    filters_right = []
    # lay cards
    for pos_x in range(boardX):
        for pos_y in range(boardY + 1):
            new_card = Card(length, pos_x, pos_y)
            cards += [new_card]
    # color left board side
    for pos_y in range(pos_y + 1):
        new_filt = Filter(length,0,pos_y)
        new_filt.choose_color(col_target)
        filters_left += [new_filt]

    for card in cards:
        left_other = get_overlap(card.pos_x, card.pos_y, cards, filters_left, filters_right=[], boardY=boardY)
        card.filter_left.calculate_color(col_target, left_other.color) #100s for testing
        card.filter_right.choose_color(col_target)

    for pos_y in range(pos_y + 1):
        new_filt = Filter(length, boardX, pos_y)
        left_other = get_overlap(boardX, pos_y, cards, filters_left, filters_right=[], boardY=boardY)
        new_filt.calculate_color(col_target, left_other)
