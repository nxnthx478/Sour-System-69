from flet import *
from time import sleep
from random import choice

from Core.Config import *
import os
from Core.Run import start_async_attacks
from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls
from Core.TBanner import banner

try:
    # start with default palette
    palette = PALETTES.get(DEFAULT_PALETTE, {'fill': ACCENT_FILL, 'stroke': ACCENT_STROKE})
    color = palette['fill']
    stroke = palette['stroke']
except:
    color = ACCENT_FILL
    stroke = ACCENT_STROKE

# custom font: if file exists, set family name (user can replace CUSTOM_FONT_PATH and name in Config)
FONT_NAME = CUSTOM_FONT_NAME if not os.path.exists(CUSTOM_FONT_PATH) else CUSTOM_FONT_NAME

def main(page: Page):
    page.window_center()
    page.title = 'SrcSys69-SmsBomber'
    page.scroll = 'adaptive'
    page.auto_scroll = True
    page.window_width = 560
    page.window_height = 600
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.theme_mode = check_config()['theme']
    page.window_maximizable = False
    page.window_resizable = False
    change_config('attack', 'False')
    # set dark cyberpunk background
    try:
        page.bgcolor = DARK_BG
    except:
        pass

    def type_attack_change(e):
        change_config('type_attack', f'{type_attack.value}')

    def feedback_change(e):
        change_config('feedback', f'{feedback.value}')

    def theme_change(e):
        # toggle theme
        page.theme_mode = 'dark' if page.theme_mode == 'light' else 'light'

        # apply background and text color
        page.bgcolor = DARK_BG if page.theme_mode == 'dark' else LIGHT_BG
        text_color = DARK_TEXT if page.theme_mode == 'dark' else LIGHT_TEXT

        # apply current palette accents (keep soft accents)
        global color, stroke
        pal = PALETTES.get(DEFAULT_PALETTE, {'fill': ACCENT_FILL, 'stroke': ACCENT_STROKE})
        # choose readable accent based on theme
        if page.theme_mode == 'light':
            color = _darken_hex(pal['fill'], 0.55)
            stroke = _darken_hex(pal['stroke'], 0.6)
        else:
            color = pal['fill']
            stroke = pal['stroke']

        # update banner with stroke + fill to ensure contrast
        try:
            # lighter stroke (smaller) and then fill text; this reduces visual heaviness
            banner.controls = [
                Text(spans=[TextSpan('SrcSys69', TextStyle(size=62, foreground=Paint(color=stroke, stroke_width=4, stroke_join='round', style='stroke')))], font_family=FONT_NAME),
                Text(spans=[TextSpan('SrcSys69', TextStyle(size=62, color=color))], font_family=FONT_NAME)
            ]
        except:
            pass

        # update controls colors safely
        try:
            number.label_style = TextStyle(color=text_color)
            number.border_color = color
            number.cursor_color = color
            replay.label_style = TextStyle(color=text_color)
            replay.border_color = color
            type_attack.label_style = TextStyle(color=text_color)
            feedback.active_color = color
            attack_button.color = color
            # animate icon change (fade/scale via animate property if supported)
            try:
                theme_button.animate = Animation(250, AnimationCurve.EASE_IN_OUT)
                theme_button.icon = icons.LIGHT_MODE if page.theme_mode == 'dark' else icons.DARK_MODE
                theme_button.icon_color = color
            except:
                theme_button.icon = icons.LIGHT_MODE if page.theme_mode == 'dark' else icons.DARK_MODE
                theme_button.icon_color = color
        except:
            pass

        # update form panel background for full theme application
        try:
            if hasattr(page, 'form_panel') and page.form_panel:
                # dark glass vs light panel
                page.form_panel.bgcolor = '#0c0c12' if page.theme_mode == 'dark' else LIGHT_BG
        except:
            pass

        page.update()
        change_config('theme', f'''{page.theme_mode}''')

    def color_change(e):
        # reapply current palette (keeps accents stable)
        global color, stroke
        pal = PALETTES.get(DEFAULT_PALETTE, {'fill': ACCENT_FILL, 'stroke': ACCENT_STROKE})
        # adapt palette for current theme for proper contrast
        if page.theme_mode == 'light':
            color = _darken_hex(pal['fill'], 0.55)
            stroke = _darken_hex(pal['stroke'], 0.6)
        else:
            color = pal['fill']
            stroke = pal['stroke']

        try:
            banner.controls = [
                Text(spans=[TextSpan('SrcSys69', TextStyle(size=62, foreground=Paint(color=stroke, stroke_width=4, stroke_join='round', style='stroke')))], font_family=FONT_NAME),
                Text(spans=[TextSpan('SrcSys69', TextStyle(size=62, color=color))], font_family=FONT_NAME)
            ]
        except:
            pass

        try:
            number.border_color = color
            number.cursor_color = color
            number.focused_border_color = color
            number.selection_color = color
            number.label_style = TextStyle(color=color)

            replay.border_color = color
            replay.cursor_color = color
            replay.focused_border_color = color
            replay.selection_color = color
            replay.label_style = TextStyle(color=color)

            type_attack.border_color = color
            type_attack.label_style = TextStyle(color=color)

            feedback.active_color = color

            attack_button.color = color
        except:
            pass

        change_config('color', f'{color}')

    # helper: lighten a hex color by amount (0..1)
    def _lighten_hex(hx: str, amount: float):
        try:
            hx = hx.lstrip('#')
            r = int(hx[0:2], 16)
            g = int(hx[2:4], 16)
            b = int(hx[4:6], 16)
            nr = int(r + (255 - r) * amount)
            ng = int(g + (255 - g) * amount)
            nb = int(b + (255 - b) * amount)
            return f"#{nr:02x}{ng:02x}{nb:02x}"
        except:
            return hx

    # darken a hex color by amount (0..1)
    def _darken_hex(hx: str, amount: float):
        try:
            hx = hx.lstrip('#')
            r = int(hx[0:2], 16)
            g = int(hx[2:4], 16)
            b = int(hx[4:6], 16)
            nr = int(r * (1 - amount))
            ng = int(g * (1 - amount))
            nb = int(b * (1 - amount))
            return f"#{nr:02x}{ng:02x}{nb:02x}"
        except:
            return hx

    def apply_palette(name: str):
        # apply palette by name and refresh UI
        global color, stroke, DEFAULT_PALETTE
        if name in PALETTES:
            DEFAULT_PALETTE = name
            pal = PALETTES[name]
            # adapt palette according to theme for readability
            if page.theme_mode == 'light':
                color = _darken_hex(pal['fill'], 0.55)
                stroke = _darken_hex(pal['stroke'], 0.6)
            else:
                color = pal['fill']
                stroke = pal['stroke']
            # update banner and controls
            try:
                banner.controls = [
                    Text(spans=[TextSpan('SrcSys69', TextStyle(size=62, foreground=Paint(color=stroke, stroke_width=4, stroke_join='round', style='stroke')))], font_family=FONT_NAME),
                    Text(spans=[TextSpan('SrcSys69', TextStyle(size=62, color=color))], font_family=FONT_NAME)
                ]
            except:
                pass
            try:
                number.border_color = color
                replay.border_color = color
                feedback.active_color = color
                attack_button.color = color
            except:
                pass
            page.update()
            change_config('color', f'{color}')

    # hover glow handlers (safe: use simple color blend to avoid API mismatches)
    def _attack_hover(e):
        try:
            if e.data:
                attack_button.color = _lighten_hex(color, 0.12)
            else:
                attack_button.color = color
            page.update()
        except:
            pass

    def _palette_hover(e):
        try:
            c = e.control
            if e.data:
                c.bgcolor = _lighten_hex(color, 0.92) if page.theme_mode == 'dark' else _lighten_hex(color, 0.96)
            else:
                c.bgcolor = None
            page.update()
        except:
            pass

    def error(message, reason='Ошибка'):
        def button_cancel(e):
            error_message.open = False
            page.update()

        error_message = AlertDialog(title=Text(reason, color=color, size=30, text_align='center', font_family=FONT_NAME), content=Text(message, font_family=FONT_NAME), actions=[TextButton('ОК', on_click=button_cancel, style=ButtonStyle(color=color))], actions_alignment='end')

        page.dialog = error_message
        error_message.open = True
        page.update()

    def start_attack():
        def button_cancel(e):
            attack_window.open = False
            page.update()

        attack_window = AlertDialog(modal=True, title=Text('Атака запущена', color=color, size=30, text_align=TextAlign.CENTER), content=ProgressBar(width=325, color=color), actions=[TextButton('Закрыть', width=90, height=40, on_click=button_cancel, style=ButtonStyle(color=color))], actions_alignment='end', open=True)

        page.dialog = attack_window
        page.update()

        change_config('attack', 'True')
        start_async_attacks(number.value, replay.value)
        change_config('attack', 'False')
        attack_window.open = False
        page.update()

    def confirmation():
        def button_cancel(e):
            confirmation_window.open = False
            page.update()

        def button_continue(e):
            confirmation_window.open = False
            page.update()
            sleep(1)
            start_attack()    


        confirmation_window = AlertDialog(modal=True, title=Text('Внимание!', color=color, size=30, text_align='center'), content=Text('После запуска атаки и её немедленной отмены процесс запуска станет необратимым, и атака всё равно будет выполнена до конца!\n\nПродолжить?'), actions=[TextButton('НЕТ', on_click=button_cancel, style=ButtonStyle(color=color)), TextButton('ДА', on_click=button_continue, style=ButtonStyle(color=color))], actions_alignment='end', open=True)
        page.dialog = confirmation_window
        page.update()

    def checking_values(e):
        if number.value:
            try:
                int(number.value)
                if number.value.isdigit() == True:
                    if replay.value:
                        try:
                            int(replay.value)
                            if replay.value.isdigit() == True:
                                if int(replay.value) > 0 and int(replay.value) < 1001:
                                    if check_config()['attack'] == 'False':
                                        confirmation()
                                    else:
                                        confirmation()
                                else:
                                    error('Введите количество повторов от 1 до 1000!')
                                    replay.focus()
                            else:
                                error('Введите количество повторов без символов!')
                                replay.focus()
                        except:
                            error('Введите количество повторов!')
                            replay.focus()
                    else:
                        error('Введите количество повторов!')
                        replay.focus()
                else:
                    error('Введите номер, только цифры!')
                    number.focus()
            except:
                error('Пожалуйста, введите корректный номер!')
                number.focus()
        else:
            error('Введите номер для атаки!')
            number.focus()

    def information(e):
        def button(ev):
            information_window.open = False
            page.update()

        information_window = AlertDialog(content=Text('SrcSys69-SmsBomber!', text_align='center', size=24, color=color, font_family=FONT_NAME), open=True, actions=[TextButton('ОК', width=110, height=50, on_click=button, style=ButtonStyle(color=color))], actions_alignment='end')
        page.dialog = information_window
        page.update()

    # banner and form fields (modern cyber/glass look)
    banner = Text('SrcSys69', size=56, color=color, font_family=FONT_NAME)

    number = TextField(label='Введите номер без "+"', width=380, text_align='center', border_radius=10, border_color=color, cursor_color=color, focused_border_color=color, autofocus=True, selection_color=color, label_style=TextStyle(color=color))

    replay = TextField(label='повторы', width=140, text_align='center', border_radius=10, border_color=color, cursor_color=color, focused_border_color=color, selection_color=color, value='1', label_style=TextStyle(color=color))

    type_attack = Dropdown(label='Тип атаки', hint_text='Выберите тип атаки', options=[dropdown.Option('MIX'), dropdown.Option('SMS'), dropdown.Option('CALL')], width=170, border_radius=10, alignment=alignment.bottom_center, border_color=color, value=check_config()['type_attack'], label_style=TextStyle(color=color), on_change=type_attack_change)

    feedback = Switch(label='Сервисы обратной связи (?)', value=True if check_config()['feedback'] == 'True' else False, width=380, active_color=color, on_change=feedback_change, tooltip='Сервисы, которые оставляют заявки (например подключение к интернету или оформление кредита) на разных сайтах. Будьте осторожны при использовании этой функции!')

    attack_button = ElevatedButton(content=Text('Запустить', size=20), on_click=checking_values, width=220, height=56, color=color)
    # attach hover glow to main action (safe: lightens the button color)
    try:
        attack_button.on_hover = _attack_hover
    except:
        pass
    # visible theme toggle button
    theme_button = IconButton(icon=icons.LIGHT_MODE if page.theme_mode == 'dark' else icons.DARK_MODE, icon_size=36, tooltip='Тема (светлая/тёмная)', on_click=theme_change, icon_color=color)

    # group controls in a centered column with banner+theme centered above
    # palette selection removed (single magenta palette)

    # bind Enter (on_submit) in number and replay to start checking/launch
    try:
        number.on_submit = checking_values
    except:
        pass
    try:
        replay.on_submit = checking_values
    except:
        pass

    def ADD():
        panel = Container(
            Column([
                Column([banner, Row([theme_button], alignment='center', spacing=12)], alignment='center', horizontal_alignment='center'),
                Text('\n'),
                Container(number, padding=padding.symmetric(vertical=6)),
                Row([type_attack, replay], alignment='CENTER', spacing=18),
                feedback,
                Container(attack_button, padding=padding.symmetric(vertical=8)),
                Row([
                    IconButton(content=Image(src='https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png', width=44, height=44), tooltip='Инстаграм', url='https://instagram.com/yourowner1488'),
                    IconButton(icon=icons.TELEGRAM, icon_size=44, tooltip='Автор', url='https://t.me/srcsys', icon_color=color),
                    IconButton(icon=icons.INFO, icon_size=44, tooltip='Информация', icon_color=color, on_click=information)
                ], alignment='CENTER', spacing=24)
            ], spacing=12, alignment='center', horizontal_alignment='center'),
            width=520,
            padding=padding.all(18),
            border_radius=14,
            bgcolor='#0c0c12'
        )

        # expose panel for theme updates and center it
        page.form_panel = panel
        page.add(Container(panel, alignment=alignment.center))

    ADD()

def Start(web=True):
    if web:
        host, port = '127.0.0.1', 9876
        banner(host, port)
        app(main, view='web_browser', host=host, port=port)
    else:
        app(main)

