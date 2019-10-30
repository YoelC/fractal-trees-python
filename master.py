import pygame
from classes.tree import Tree
from ui.button import Button
from ui.slider import Slider
from ui.checkbox import CheckBox
from multifile import WINDOW_WIDTH, WINDOW_HEIGHT
import os

pygame.init()
CLOCK = pygame.time.Clock()
FPS = 30

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Values start maxed out
tree_parameters = {
    'pos': ((WINDOW_WIDTH - 400) / 2 + 400, WINDOW_HEIGHT),
    'angle': 90,
    'tick': 15,
    'vel': 10,
    'number': 14,
    'division_ratio': 2,
    'division_angle': 90,
    'divide_angles': True,
    'divide_distance': True,
    'fruits': False
}

buttons = {
    'button_reset': Button((50, WINDOW_HEIGHT - 125, 300, 75), 'Reset', outline_width=4),
    'button_hide': Button((415, 25, 25, 25), '<', size=30, outline_width=2)

}

sliders = {
    'slider_number': Slider((50, WINDOW_HEIGHT - 225, 300, 75), 'Divisions', tree_parameters['number']),
    'slider_division_ratio': Slider((50, WINDOW_HEIGHT - 350, 300, 75), 'Division Ratio', tree_parameters['division_ratio']),
    'slider_division_angle': Slider((50, WINDOW_HEIGHT - 475, 300, 75), 'Division Angle', tree_parameters['division_angle'])
}

checkboxes = {
    'checkbox_divide_angles': CheckBox((50, 200), 'Divide Angles'),
    'checkbox_divide_distance': CheckBox((50, 125), 'Divide Distance'),
    'checkbox_fruits': CheckBox((50, 50), "Spawn 'Fruits'")
}
checkboxes['checkbox_divide_angles'].checked = True
checkboxes['checkbox_divide_distance'].checked = True

sliders['slider_number'].set_round(0)
sliders['slider_division_ratio'].set_percentage(60)
sliders['slider_division_angle'].set_percentage(37)
sliders['slider_number'].set_percentage(85)


tree_parameters['number'] = sliders['slider_number'].get_value()
tree_parameters['division_ratio'] = sliders['slider_division_ratio'].get_value()
tree_parameters['division_angle'] = sliders['slider_division_angle'].get_value()

tree1 = Tree(pos=tree_parameters['pos'],
             angle=tree_parameters['angle'],
             ticks=tree_parameters['tick'],
             vel=tree_parameters['vel'],
             number=tree_parameters['number'],
             division_ratio=tree_parameters['division_ratio'],
             division_angle=tree_parameters['division_angle'],
             divide_angles=tree_parameters['divide_angles'],
             divide_distance=tree_parameters['divide_distance'],
             fruits=tree_parameters['fruits'])

mouse_pos = None

clicked = False
holding_click = False
hidden_hud = False

run = True
while run:
    clicked = False
    if pygame.mouse.get_pressed()[0] == 1 and not holding_click:
        clicked = True
        holding_click = True

    if pygame.mouse.get_pressed()[0] == 0:
        holding_click = False

    CLOCK.tick(FPS)
    run = False if pygame.QUIT in [event.type for event in pygame.event.get()] else True
    pygame.display.set_caption(f'fps: {CLOCK.get_fps()}')

    if hidden_hud:
        for slider in sliders:
            sliders[slider].move_frame((-415, 0))
        for button in buttons:
            buttons[button].move_frame((-415, 0))
        for checkbox in checkboxes:
            checkboxes[checkbox].move_frame((-415, 0))

        buttons['button_hide'].text = '>'
        buttons['button_hide'].move_frame((-407.5, 0))

        tree_parameters['pos'] = (WINDOW_WIDTH / 2, WINDOW_HEIGHT)
    else:
        tree_parameters['pos'] = ((WINDOW_WIDTH - 400) / 2 + 400, WINDOW_HEIGHT)
        buttons['button_hide'].text = '<'

    tree_parameters['number'] = sliders['slider_number'].get_value()
    tree_parameters['division_ratio'] = sliders['slider_division_ratio'].get_value() if sliders['slider_division_ratio'].get_value() != 0 else 0.1
    tree_parameters['division_angle'] = sliders['slider_division_angle'].get_value()
    tree_parameters['divide_angles'] = checkboxes['checkbox_divide_angles'].is_checked()
    tree_parameters['divide_distance'] = checkboxes['checkbox_divide_distance'].is_checked()
    tree_parameters['fruits'] = checkboxes['checkbox_fruits'].is_checked()

    if pygame.key.get_pressed()[pygame.K_r]:
        tree1 = Tree(pos=tree_parameters['pos'],
                     angle=tree_parameters['angle'],
                     ticks=tree_parameters['tick'],
                     vel=tree_parameters['vel'],
                     number=tree_parameters['number'],
                     division_ratio=tree_parameters['division_ratio'],
                     division_angle=tree_parameters['division_angle'],
                     divide_angles=tree_parameters['divide_angles'],
                     divide_distance=tree_parameters['divide_distance'],
                     fruits=tree_parameters['fruits'])

    if clicked:
        if buttons['button_reset'].check_clicked():
            tree1 = Tree(pos=tree_parameters['pos'],
                         angle=tree_parameters['angle'],
                         ticks=tree_parameters['tick'],
                         vel=tree_parameters['vel'],
                         number=tree_parameters['number'],
                         division_ratio=tree_parameters['division_ratio'],
                         division_angle=tree_parameters['division_angle'],
                         divide_angles=tree_parameters['divide_angles'],
                         divide_distance=tree_parameters['divide_distance'],
                         fruits=tree_parameters['fruits'])
        for checkbox in checkboxes:
            if checkboxes[checkbox].check_clicked():
                checkboxes[checkbox].checked = not checkboxes[checkbox].checked
        if buttons['button_hide'].check_clicked():
            hidden_hud = not hidden_hud

    for slider in sliders:
        sliders[slider].check_clicked(clicked, holding_click)
        sliders[slider].move(pygame.mouse.get_pos()[0])

    if not any([sliders[slider].holding_click for slider in sliders]):
        if pygame.mouse.get_pressed()[0] == 1:
            previous_mouse_pos = mouse_pos
            mouse_pos = pygame.mouse.get_pos()

            if mouse_pos != previous_mouse_pos and previous_mouse_pos is not None:
                dx = mouse_pos[0] - previous_mouse_pos[0]
                dy = mouse_pos[1] - previous_mouse_pos[1]
                tree1.move_center(dx, dy)

        elif pygame.mouse.get_pressed()[0] == 0:
            mouse_pos = None

    tree1.create_new()

    tree1.move()

    win.fill((64, 64, 64))
    tree1.draw(win)
    if not hidden_hud:
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 455, WINDOW_HEIGHT))
    else:
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 40, WINDOW_HEIGHT))

    for button in buttons:
        buttons[button].draw(win)
    for slider in sliders:
        sliders[slider].draw(win)
    for checkbox in checkboxes:
        checkboxes[checkbox].draw(win)
    pygame.display.flip()
