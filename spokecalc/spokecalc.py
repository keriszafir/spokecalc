#!/usr/bin/env python3

# Spoke length calculator

from math import sqrt, cos, pi


def enter_data_spec_type_or_blank(prompt, datatype):
    """enter_data_spec_type_or_blank:

    Enter a value or leave blank, try to convert to the specified datatype
    """
    value = input(prompt)
    try:
        return datatype(value)
    except ValueError:
        return value


def simple_menu(message, options):
    """Simple menu:

    A simple menu where user is asked what to do.
    Wrong choice points back to the menu.

    Message: string displayed on screen;
    options: a list or tuple of strings - options.
    """
    ans = ''
    while True:
        ans = input(message)
        if ans in options:
            return options[ans]
        elif ans.lower() in options:
            return options[ans.lower()]
        elif ans.upper() in options:
            return options[ans.upper()]
        else:
            pass


def yes_or_no(question):
    """yes_or_no

    Asks a simple question with yes or no answers.
    Returns True for yes and False for no.
    """
    return simple_menu('%s [Y / N]: ' % question, {'Y': True, 'N': False})


def calculate(left_hub_diameter, right_hub_diameter, rim_diameter,
              hole_diameter, spokes_left, spokes_right,
              crosses_left, crosses_right, left_dist, right_dist):
    """calculate:

    Calculates the left and right side spoke lengths for given parameters:
    left_hub_diameter - pitch circle diameter for left side,
    right_hub_diameter - pitch circle diameter for right side,
    rim_diameter - effective rim diameter (ERD),
    hole_diameter - hub hole diameter,
    spokes_left, spokes_right - spokes number for left / right side
    crosses_left, crosses_right - no of crosses on left / right side of wheel,
    left_dist, right_dist - flange to wheel's symmetry plane distances.

    Returns (left_spoke_length, right_spoke_length).
    """
    # For simplicity's sake let's calculate these first
    rim_r = rim_diameter / 2
    left_hub_r = left_hub_diameter / 2
    right_hub_r = right_hub_diameter / 2
    hole_r = hole_diameter / 2
    left_theta = 2 * pi * crosses_left / spokes_left
    right_theta = 2 * pi * crosses_right / spokes_right
    # Now calculate the intermediate lengths - on a flat circle
    l_int_length = sqrt((left_hub_r ** 2) + (rim_r ** 2) -
                        (2 * rim_r * left_hub_r * cos(left_theta)))
    r_int_length = sqrt((right_hub_r ** 2) + (rim_r ** 2) -
                        (2 * rim_r * right_hub_r * cos(right_theta)))
    # Correct for the hub flange-to-center distances
    left_length = sqrt((left_dist ** 2) + (l_int_length ** 2)) - hole_r
    right_length = sqrt((right_dist ** 2) + (r_int_length ** 2)) - hole_r
    # Ready; return the lengths
    return (left_length, right_length)


def main():
    prompt = 'Left hub flange pitch circle diameter [mm]? (default: 58mm) : '
    left_hub_diameter = enter_data_spec_type_or_blank(prompt, float) or 58
    prompt = ('Right hub flange pitch circle diameter [mm]? '
              '(default: the same as left) : ')
    right_hub_diameter = (enter_data_spec_type_or_blank(prompt, float) or
                          left_hub_diameter)
    prompt = 'Effective rim diameter [mm]? (default: 608) : '
    rim_diameter = enter_data_spec_type_or_blank(prompt, float) or 608
    prompt = 'Does the wheel have the same number of spokes on both sides?'
    if yes_or_no(prompt):
        prompt = 'How many spokes? (default: 36) : '
        spokes = enter_data_spec_type_or_blank(prompt, int) or 36
        spokes_left = spokes / 2
        spokes_right = spokes / 2
    else:
        prompt = 'How many spokes on the left side? (default: 18) : '
        spokes_left = enter_data_spec_type_or_blank(prompt, int) or 18
        prompt = 'How many spokes on the right side? (default: 18) : '
        spokes_right = enter_data_spec_type_or_blank(prompt, int) or 18
    prompt = 'Left side hub flange-to-center distance [mm]? (default: 25) : '
    left_dist = enter_data_spec_type_or_blank(prompt, float) or 25
    prompt = ('Right side hub flange-to-center distance [mm]? '
              '(default: the same as left) : ')
    right_dist = enter_data_spec_type_or_blank(prompt, float) or left_dist
    prompt = 'Hub hole diameter [mm]? (default: 2.7) : '
    hole_diameter = enter_data_spec_type_or_blank(prompt, float) or 2.7
    prompt = 'Crosses on the left side? (default: 3) : '
    crosses_left = enter_data_spec_type_or_blank(prompt, int) or 3
    prompt = 'Crosses on the right side? (default: same as the left) : '
    crosses_right = enter_data_spec_type_or_blank(prompt, int) or crosses_left
    print('We now have all data, calculating the length...')
    result = calculate(left_hub_diameter, right_hub_diameter, rim_diameter,
                       hole_diameter, spokes_left, spokes_right,
                       crosses_left, crosses_right, left_dist, right_dist)
    print('Left spokes length: %s' % result[0])
    print('Right spokes length: %s' % result[1])
    input('[Enter] to start all over, [ctrl-C] to exit...')


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\n\nThank you and goodbye!\n')
        exit()
