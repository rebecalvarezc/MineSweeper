def movement_menu():
    print('''From your position, you can execute the following actions:
            1) w = move up
            2) s = move down
            3) a = move left
            4) d = move right
            5) m = flag a square
            6) n = unflag a square
            7) z = open a square
            ''')
    movement = input('Indicate the movement you want to make: \n--> ').lower()
    return movement
