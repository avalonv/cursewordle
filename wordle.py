#!/usr/bin/env python3
from const import *
from sys import argv
import input as input
import output as out
import curses

is_daily = False
# max space between letters, actual space depends on screen size
spacing = 3


def win_size_wrapper(stdscr):
    global spacing
    set_colors()
    # this will catch the very useful and informative 'curses.error'
    # when foolishly attempting to create windows larger than the
    # screen (i.e. the whole terminal), and reduce the spacing
    # between chars (and thus size of the windows) until it fits.
    # it will also catch other, equally important errors, with
    # equally informative names, so it's best to call set_win_size
    # directly if debugging
    while True:
        if spacing >= 1:
            try:
                windows = set_win_size(stdscr, spacing, True, is_daily)
                break
            except curses.error:
                spacing -= 1
        else:
            raise OverflowError
    return windows


def game(stdscr, solution):
    scorewin, msgwin, kbwin = win_size_wrapper(stdscr)

    guessed_words = []
    kb_dic = alphabet
    while len(guessed_words) < max_guesses:
        out.update_kb(kbwin, kb_dic)
        user_input = input.echo_str(scorewin, len(guessed_words), spacing)
        if user_input in valid_words:
            current_guess = input.compare_word(user_input, solution, kb_dic)
            guessed_words.append(current_guess)
            scorewin.refresh()
            # only refresh 'word not in list'
            # message if new input passes
            msgwin.clear()
            msgwin.refresh()
            if current_guess[0] == solution:
                out.update_kb(kbwin, kb_dic)
                out.update_words(scorewin, guessed_words, spacing)
                out.end_score(msgwin, win=True, result=len(guessed_words))
                stdscr.getkey()
                return 0
        else:
            out.color_str(msgwin, 'Word not in list.', 1, 0, grey)
            msgwin.refresh()
        out.update_kb(kbwin, kb_dic)
        out.update_words(scorewin, guessed_words, spacing)

    out.end_score(msgwin, win=False, result=solution)
    stdscr.getkey()
    return 1


if __name__ == '__main__':
    if len(argv) > 1:
        arg = argv[1].rstrip().lower()
        if arg == "--nyt":
            solution = set_nyt_word()
            is_daily = True
        elif len(arg) == word_len and arg in valid_words:
            solution = arg
        else:
            print(f"Word not in list")
            exit(2)
    else:
        solution = set_random_word()
        daily_word = 0
    try:
        exit(curses.wrapper(game, solution))
    except KeyboardInterrupt:
        exit(0)
    except OverflowError:
        print("Couldn't start display.")
        print("Window needs to be at least 27x16")
        exit(2)
