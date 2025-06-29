import curses
from data.const import menu_items


def menu(stdscr: curses.window):
    stdscr.clear()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    options = menu_items
    current_row = 0

    while True:
        for idx, action in enumerate(options):
            if idx == current_row:
                stdscr.addstr(idx, 0, f'-> {action["name"]}', curses.color_pair(1))

                stdscr.move(len(options), 0)
                stdscr.clrtoeol()

                stdscr.addstr(len(options), 0, f'{action["description"]}', curses.color_pair(2))
            else:
                stdscr.addstr(idx, 0, f'   {action["name"]}')

        stdscr.refresh()
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            if current_row > 0:
                current_row -= 1
            else:
                current_row = len(options) - 1
        elif key == curses.KEY_DOWN:
            if current_row < len(options) - 1:
                current_row += 1
            else:
                current_row = 0
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return current_row