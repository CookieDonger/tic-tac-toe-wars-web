# Checking if offense can make the move
def check_legal(board, i, j):
    if i == 0:
        # Literal top left corner case
        if j == 0:
            if board[i][j + 1] == 1 or board[i + 1][j] == 1 or board[i + 1][j + 1] == 1:
                return True
        # Top right corner case
        elif j == 5:
            if board[i][j - 1] == 1 or board[i + 1][j] == 1 or board[i + 1][j - 1] == 1:
                return True
        # Rest of top edge
        else:
            if board[i][j - 1] == 1 or board[i][j + 1] == 1 or board[i + 1][j - 1] == 1 or board[i + 1][j] == 1 or board[i + 1][j + 1] == 1:
                return True
    # Bottom edge
    elif i == 5:
        # Bottom left corner case
        if j == 0:
            if board[i][j + 1] == 1 or board[i - 1][j] == 1 or board[i - 1][j + 1] == 1:
                return True
        # Bottom right corner case
        elif j == 5:
            if board[i][j - 1] == 1 or board[i - 1][j] == 1 or board[i - 1][j - 1] == 1:
                return True
        # Rest of bottom edge
        else:
            if board[i][j - 1] == 1 or board[i][j + 1] == 1 or board[i - 1][j - 1] == 1 or board[i - 1][j] == 1 or board[i - 1][j + 1] == 1:
                return True
    # Left edge
    elif j == 0:
        # Making sure to not do corners
        if i != 0 and i != 5:
            if board[i - 1][j + 1] == 1 or board[i][j + 1] == 1 or board[i + 1][j + 1] == 1 or board[i - 1][j] == 1 or board[i + 1][j] == 1:
                return True
    # Right edge
    elif j == 5:
        # Making sure to not do corners
        if i != 0 and i != 5:
            if board[i - 1][j - 1] == 1 or board[i][j - 1] == 1 or board[i + 1][j - 1] == 1 or board[i - 1][j] == 1 or board[i + 1][j] == 1:
                return True
    # Rest of board
    else:
        # Should be 8 total conditionals as there are 8 bordering squares
        if board[i - 1][j - 1] == 1 or board[i][j - 1] == 1 or board[i + 1][j - 1] == 1:
            return True
        if board[i - 1][j] == 1 or board[i + 1][j] == 1:
            return True
        if board[i - 1][j + 1] == 1 or board[i][j + 1] == 1 or board[i + 1][j + 1] == 1:
            return True
    return False


# Checking if offense can make a move
def check_possible(board):
    for i in range(6):
        for j in range(6):
            # Checking board for squares that have offense
            if board[i][j] == 1:
                # Top edge
                if i == 0:
                    # Literal top left corner case
                    if j == 0:
                        if board[i][j + 1] == 0 or board[i + 1][j] == 0 or board[i + 1][j + 1] == 0:
                            return True
                    # Top right corner case
                    elif j == 5:
                        if board[i][j - 1] == 0 or board[i + 1][j] == 0 or board[i + 1][j - 1] == 0:
                            return True
                    # Rest of top edge
                    else:
                        if board[i][j - 1] == 0 or board[i][j + 1] == 0 or board[i + 1][j - 1] == 0 or board[i + 1][j] == 0 or board[i + 1][j + 1] == 0:
                            return True
                # Bottom edge
                elif i == 5:
                    # Bottom left corner case
                    if j == 0:
                        if board[i][j + 1] == 0 or board[i - 1][j] == 0 or board[i - 1][j + 1] == 0:
                            return True
                    # Bottom right corner case
                    elif j == 5:
                        if board[i][j - 1] == 0 or board[i - 1][j] == 0 or board[i - 1][j - 1] == 0:
                            return True
                    # Rest of bottom edge
                    else:
                        if board[i][j - 1] == 0 or board[i][j + 1] == 0 or board[i - 1][j - 1] == 0 or board[i - 1][j] == 0 or board[i - 1][j + 1] == 0:
                            return True
                # Left edge
                elif j == 0:
                    # Making sure to not do corners
                    if i != 0 and i != 5:
                        if board[i - 1][j + 1] == 0 or board[i][j + 1] == 0 or board[i + 1][j + 1] == 0 or board[i - 1][j] == 0 or board[i + 1][j] == 0:
                            return True
                # Right edge
                elif j == 5:
                    # Making sure to not do corners
                    if i != 0 and i != 5:
                        if board[i - 1][j - 1] == 0 or board[i][j - 1] == 0 or board[i + 1][j - 1] == 0 or board[i - 1][j] == 0 or board[i + 1][j] == 0:
                            return True
                # Rest of board
                else:
                    # Should be 8 total conditionals as there are 8 bordering squares
                    if board[i - 1][j - 1] == 0 or board[i][j - 1] == 0 or board[i + 1][j - 1] == 0:
                        return True
                    if board[i - 1][j] == 0 or board[i + 1][j] == 0:
                        return True
                    if board[i - 1][j + 1] == 0 or board[i][j + 1] == 0 or board[i + 1][j + 1] == 0:
                        return True
    return False


# Checking score everytime a move is played
def check_score(board, side):
    score = 0
    # Splitting this into horizontal, vertical, four corners, and illuminati
    score += horizontal_check(board, side)
    score += vertical_check(board, side)
    score += diagonal_check_1(board, side)
    score += diagonal_check_2(board, side)
    score += four_corners_check(board, side)
    score += illuminati_check(board, side)
    return score


# Horizontal check
def horizontal_check(board, side):
    score = 0
    if side == "offense":
        num = 1
    else:
        num = 2
    for i in range(6):
        connect = 0
        # Start at middle because without those squares there is no possible way to score
        if board[i][2] == num and board[i][3] == num:
            connect = 2
            if board[i][1] == num:
                connect += 1
                if board[i][0] == num:
                    connect += 1
            if board[i][4] == num:
                connect += 1
                if board[i][5] == num:
                    connect += 1
        # Scoring
        if connect >= 6:
            score += 5
        elif connect >= 5:
            score += 2
        elif connect >= 4:
            score += 1
    return score


# Vertical Check
def vertical_check(board, side):
    score = 0
    if side == "offense":
        num = 1
    else:
        num = 2
    for i in range(6):
        connect = 0
        # Start at middle as well because without those squares there is no possible way to score
        if board[2][i] == num and board[3][i] == num:
            connect = 2
            if board[1][i] == num:
                connect += 1
                if board[0][i] == num:
                    connect += 1
            if board[4][i] == num:
                connect += 1
                if board[5][i] == num:
                    connect += 1
        # Scoring
        if connect >= 6:
            score += 5
        elif connect >= 5:
            score += 2
        elif connect >= 4:
            score += 1
    return score


# Diagonal Check for top left to bottom right
def diagonal_check_1(board, side):
    score = 0
    if side == "offense":
        num = 1
    else:
        num = 2
    # Range 5 because the last square can't be this diagonal
    for i in range(5):
        connect = 0
        # Top left to Bottom right diagonals
        if board[2][i] == num:
            connect = 1
            # Making sure element index exists
            if 0 <= i + 1 <= 5:
                if board[3][i + 1] == num:
                    connect += 1
                    if 0 <= i + 2 <= 5:
                        if board[4][i + 2] == num:
                            connect += 1
                        if 0 <= i + 3 <= 5:
                            if board[5][i + 3] == num:
                                connect += 1
                    if 0 <= i - 1 <= 5:
                        if board[1][i - 1] == num:
                            connect += 1
                            if 0 <= i - 2 <= 5:
                                if board[0][i - 2] == num:
                                    connect += 1
        # Scoring
        if connect >= 6:
            score += 5
        elif connect >= 5:
            score += 2
        elif connect >= 4:
            score += 1
    return score


# Diagonal Check for top right to bottom left
def diagonal_check_2(board, side):
    score = 0
    if side == "offense":
        num = 1
    else:
        num = 2
    # Range 5 again for the same reason
    for i in range(5):
        connect = 0
        # Top left to Bottom right diagonals
        if board[3][i] == num:
            connect = 1
            # Making sure element index exists
            if 0 <= i + 1 <= 5:
                if board[2][i + 1] == num:
                    connect += 1
                    if 0 <= i + 2 <= 5:
                        if board[1][i + 2] == num:
                            connect += 1
                        if 0 <= i + 3 <= 5:
                            if board[0][i + 3] == num:
                                connect += 1
                    if 0 <= i - 1 <= 5:
                        if board[4][i - 1] == num:
                            connect += 1
                            if 0 <= i - 2 <= 5:
                                if board[5][i - 2] == num:
                                    connect += 1
        # Scoring
        if connect >= 6:
            score += 5
        elif connect >= 5:
            score += 2
        elif connect >= 4:
            score += 1
    return score


# Four Corners
def four_corners_check(board, side):
    score = 0
    if side == "offense":
        num = 1
    else:
        num = 2
    # Just check if the player has all 4 corners
    if board[0][0] == num:
        if board[0][5] == num:
            if board[5][0] == num:
                if board[5][5] == num:
                    score += 1
    return score


def illuminati_check(board, side):
    score = 0
    if side == "offense":
        num = 1
        num2 = 2
    else:
        num = 2
        num2 = 1
    for i in range(6):
        for j in range(6):
            if board[i][j] == num:
                # Checking if vertex can be top left triangle
                if 0 <= i - 3 and 0 <= j - 3:
                    # Vertical Check
                    if board[i - 1][j] == num and board[i - 2][j] == num and board[i - 3][j] == num:
                        # Horizontal Check
                        if board[i][j - 1] == num and board[i][j - 2] == num and board[i][j - 3] == num:
                            # Diagonal Check and if it's surrounding an opposing mark
                            if board[i - 2][j - 1] == num and board[i - 1][j - 2] == num and board[i - 1][j - 1] == num2:
                                score += 3
                # Checking if vertex can be top right triangle
                elif 0 <= i - 3 and 5 >= j + 3:
                    # Vertical Check
                    if board[i - 1][j] == num and board[i - 2][j] == num and board[i - 3][j] == num:
                        # Horizontal Check
                        if board[i][j + 1] == num and board[i][j + 2] == num and board[i][j + 3] == num:
                            # Diagonal Check and if it's surrounding an opposing mark
                            if board[i - 2][j + 1] == num and board[i - 1][j + 2] == num and board[i - 1][j + 1] == num2:
                                score += 3
                # Checking if vertex can be bottom left triangle
                elif 5 >= i + 3 and 0 <= j - 3:
                    # Vertical Check
                    if board[i + 1][j] == num and board[i + 2][j] == num and board[i + 3][j] == num:
                        # Horizontal Check
                        if board[i][j - 1] == num and board[i][j - 2] == num and board[i][j - 3] == num:
                            # Diagonal Check and if it's surrounding an opposing mark
                            if board[i + 2][j - 1] == num and board[i + 1][j - 2] == num and board[i + 1][j - 1] == num2:
                                score += 3
                # Checking if vertex can be bottom right triangle
                elif 5 >= i + 3 and 5 >= j + 3:
                    # Vertical Check
                    if board[i + 1][j] == num and board[i + 2][j] == num and board[i + 3][j] == num:
                        # Horizontal Check
                        if board[i][j + 1] == num and board[i][j + 2] == num and board[i][j + 3] == num:
                            # Diagonal Check and if it's surrounding an opposing mark
                            if board[i + 2][j + 1] == num and board[i + 1][j + 2] == num and board[i + 1][j + 1] == num2:
                                score += 3
    return score


def end_game(game, gameboard):
    # Giving the empty squares to defense
    for i in range(6):
        for j in range(6):
            if gameboard[i][j] == 0:
                gameboard[i][j] = 2

    # Score Check
    # For games 1, 3, 5
    if game.gamenumber in [1, 3, 5]:
        # Score check after giving defense squares
        game.score1 = check_score(gameboard, "offense")
        game.score2 = check_score(gameboard, "defense")
    # For games 2, 4, 6
    else:
        game.score1 = check_score(gameboard, "defense")
        game.score2 = check_score(gameboard, "offense")
    game.matchscore1 = game.score1 + game.matchscore1
    game.matchscore2 = game.score2 + game.matchscore2

    # Recording board and score for the game
    # Recording which board based on the game number
    if game.gamenumber == 1:
        game.board1 = gameboard
        game.p1game1score = game.matchscore1
        game.p2game1score = game.matchscore2
    elif game.gamenumber == 2:
        game.board2 = gameboard
        game.p1game2score = game.matchscore1
        game.p2game2score = game.matchscore2
    elif game.gamenumber == 3:
        game.board3 = gameboard
        game.p1game3score = game.matchscore1
        game.p2game3score = game.matchscore2
    elif game.gamenumber == 4:
        game.board4 = gameboard
        game.p1game4score = game.matchscore1
        game.p2game4score = game.matchscore2
    elif game.gamenumber == 5:
        game.board5 = gameboard
        game.p1game5score = game.matchscore1
        game.p2game5score = game.matchscore2
    else:
        game.board6 = gameboard
        game.p1game6score = game.matchscore1
        game.p2game6score = game.matchscore2

    # Resetting the board or ending the match
    # If it's not game 6, then reset board and set up for next game
    if game.gamenumber < 6:
        game.gamenumber += 1
        # Setting up the next game, switching sides and all
        game.score1 = 0
        game.score2 = 0
        game.movecount = 0
    # If it's game 6, then end the entire match
    else:
        game.active = False
        if game.matchscore1 > game.matchscore2:
            game.winner = game.p1
            newrating = game.p1.rating + 8
            game.p1.rating = newrating
            newrating = game.p2.rating - 8
            game.p2.rating = newrating
        elif game.matchscore1 < game.matchscore2:
            game.winner = game.p2
            newrating = game.p1.rating - 8
            game.p1.rating = newrating
            newrating = game.p2.rating + 8
            game.p2.rating = newrating
    game.p1.save()
    game.p2.save()
    game.save()
    return game
