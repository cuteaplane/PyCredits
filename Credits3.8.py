import time
import sys
import os
import pygame.mixer # pygame 模块: pip install pygame

class Credits_BGA:

    bpm = 179
    beat_time = 60 / bpm
    half_beat_time = 60 / bpm / 2
    quarter_beat_time = 60 / bpm / 4
    half_quarter_beat_time = 60 / bpm / 8

    # --- 关于特殊字符的重要说明 (更新) ---
    # 原始代码使用了 \xNN 形式的转义。在 Python 3 中，这代表 Unicode U+00NN。
    # 原始代码想要的是 CP437 编码（一种旧的字符编码，常用于DOS界面的图形），
    # 所以换字体是必要的。

    # 块状阴影字符 (转为 Unicode)
    light = '\u2591'  # ░ (浅色阴影)，原为 '\xb0' (U+00B0 = ° 度数符号)
    median = '\u2592' # ▒ (中等阴影)，原为 '\xb1' (U+00B1 = ± 加减号)
    dark = '\u2593'   # ▓ (深色阴影)，原为 '\xb2' (U+00B2 = ² 上标2)

    # 其他符号 (保留 \xNN)
    
    smile = '\xb3'
    # '\xb4' (U+00B4) 是 '´' (锐音符)。CP437: '┤' (U+2524)。若需八分音符 '♪'，用 '\u266A'。
    eighth_note = '\xb4'
    # '\xb5' (U+00B5) 是 'µ' (微符号)。CP437: '╡' (U+252C)。若需十六分音符 '♬'，用 '\u266C'。
    sixteenth_note = '\xb5'

    # --- 新增的 CP437 特殊字符处理 (来自 _5, _6, _7 方法) ---
    # 这些字符在 CP437 中用于绘制边框和特殊符号
    # 我把这些这转成了对应的 Unicode （由于一些奇怪问题）


    # CP437 Box Drawing and Symbols to Unicode:
    cp437_to_unicode = {
        0xaf: '\u2192', # → (右箭头), 原 CP437 应该是 'X' with overline, or custom. Using right arrow as placeholder for 'pointer'.
        0xb3: '\u2502', # │ Box Drawings Light Vertical (Note: self.smile uses '\xb3' for '³')
        0xb6: '\u00B6', # ¶ (Pilcrow sign), CP437: ' సౌ' (Telugu letter SA + Vowel sign AU) - This seems unlikely. Assuming it was a custom char.
        0xba: '\u2551', # ║ Box Drawings Double Vertical
        0xbb: '\u2557', # ╗ Box Drawings Double Down and Left
        0xbc: '\u255D', # ╝ Box Drawings Double Up and Left
        0xc4: '\u2500', # ─ Box Drawings Light Horizontal
        0xc7: '\u2560', # ╠ Box Drawings Double Vertical and Right
        0xc8: '\u255A', # ╚ Box Drawings Double Up and Right
        0xc9: '\u2554', # ╔ Box Drawings Double Down and Right
        0xcd: '\u2550', # ═ Box Drawings Double Horizontal
        0xcf: '\u2569', # ╩ Box Drawings Double Up and Horizontal
        0xd1: '\u2566', # ╦ Box Drawings Double Down and Horizontal
        0xdf: '\u2580', # ▀ Upper Half Block
        0xea: '\u00EA', # ê (Latin small letter e with circumflex), CP437: Ω (Omega)
        0xf1: '\u00F1', # ñ (Latin small letter n with tilde), CP437: ± (Plus-minus sign)
        0xf7: '\u00F7', # ÷ (Division sign), CP437: ≈ (Almost equal to)
        0x7c: '\u2502', # │ (Vertical bar on keyboard, often maps to Box Drawings Light Vertical in terminals)
        # Characters from _6 method's inv_cop string:
        # 0x2c6: '\u02C6', # ˆ (Modifier Letter Circumflex Accent) # These are already Unicode via chr()
        # 0x2021: '\u2021',# ‡ (Double Dagger)
        # 0x2030: '\u2030',# ‰ (Per Mille Sign)
        # 0x2020: '\u2020',# † (Dagger)
        # 0x2026: '\u2026',# … (Horizontal Ellipsis)
        # Characters from _6 method's f-string formatting:
        0xa6: '\u00A6', # ¦ (Broken Bar)
        0xa7: '\u00A7', # § (Section Sign)
        0xab: '\u00AB', # « (Left-Pointing Double Angle Quotation Mark)
        0xac: '\u00AC', # ¬ (Not Sign)
        0xae: '\u00AE', # ® (Registered Sign)
    }

    # Helper to convert if needed, or keep original if not in map
    def _uc(self, char_code_or_str):
        if isinstance(char_code_or_str, int):
            # For things like 0xb3, if it's meant for box drawing, use the map.
            # self.smile is also '\xb3' but means '³'. 
            # Remember to use correct font.     
            # This helper is mostly for explicit CP437 box codes.
            return self.cp437_to_unicode.get(char_code_or_str, chr(char_code_or_str))
        # If it's already a string (like \xea from original code), Python 3 \xNN is already a Unicode char.
        # We assume these are intended as their direct Unicode U+00NN values if not in the map.
        # e.g. self._uc('\xea') will just return '\xea' (ê)
        return char_code_or_str


    def __init__(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        pygame.mixer.init()
        try:
            pygame.mixer.music.load('credits.mp3')
        except pygame.error as e:
            print(f"错误：无法加载 'credits.mp3'。 {e}")
            print("继续播放，但没有背景音乐")

        time.sleep(1)
        print('\x1b[?25l', end='')
        sys.stdout.flush()

        # Check if mixer is initialized and music isn't already playing to avoid errors
        if pygame.mixer.get_init() and not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.play(start=0)
            except pygame.error as e:
                print(f"播放音乐时出错: {e}")


        self._1()
        self._2()
        self._3()
        self._4()
        self._5()
        self._6()
        self._7()
        self._8()

        print('\x1b[?25h', end='')
        sys.stdout.flush()
        if pygame.mixer.get_init():
            pygame.mixer.music.fadeout(500)
            time.sleep(0.5)
            pygame.mixer.quit()
        print("\nCredits BGA 播放完毕！ (^_^)/~~")


    def output(self, text:str, wait_time:float):
        sys.stdout.write('\033[2J')
        sys.stdout.write('\033[H')
        sys.stdout.write(text)
        sys.stdout.flush()
        time.sleep(wait_time)

    def _1(self):
        frames = {
            "beginning1":'THE BMS FIGHTER ULTIMATE\n\n               Smith au Lait',
            "beginning2":'THE BMS FIGHTER ULTIMATE\n\n               Smith au Lait\n\nMusic: Frums\n\n                  BGA: Frums',
            "beginning3":'THE BMS FIGHTER ULTIMATE\n\n               Smith au Lait\n\nMusic: Frums\n\n                  BGA: Frums\n\nGenre: OTHER TIME\n\n                    BPM: 179',
            "beginning4":'THE BMS FIGHTER ULTIMATE\n\n               Smith au Lait\n\nMusic: Frums\n\n                  BGA: Frums\n\nGenre: OTHER TIME\n\n                    BPM: 179\n\nCredits',
            "01":' 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 \n'*7,
            "02":'0 0 0 0 0 0 0 0 0 0 0 0 0 0 \n 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n'*7
        }

        def _animate_zeros():
            for _ in range(4):
                self.output(frames['01'], self.quarter_beat_time)
                self.output(frames['02'], self.quarter_beat_time)

        self.output(frames['beginning1'], 6*self.beat_time)
        _animate_zeros()
        self.output(frames['beginning2'], 6*self.beat_time)
        _animate_zeros()
        self.output(frames['beginning3'], 6*self.beat_time)
        _animate_zeros()
        self.output(frames['beginning4'], 6*self.beat_time)
        _animate_zeros()

    def _2(self):
        def ender_pearl(char:str, type:bool, wait_time:float):
            if type == False:
                self.output(f'Credits\n\n            {2*self.eighth_note}{2*self.sixteenth_note}\n        {6*self.eighth_note}{6*self.sixteenth_note}\n      {8*self.eighth_note}{8*self.sixteenth_note}\n      {6*self.eighth_note}{4*char}{6*self.sixteenth_note}\n    {6*self.eighth_note}{8*char}{6*self.sixteenth_note}\n    {6*self.sixteenth_note}{8*char}{6*self.eighth_note}\n      {6*self.sixteenth_note}{4*char}{6*self.eighth_note}\n      {8*self.sixteenth_note}{8*self.eighth_note}\n        {6*self.sixteenth_note}{6*self.eighth_note}\n            {2*self.sixteenth_note}{2*self.eighth_note}\n\n                       Frums', wait_time)
            elif type == True:
                self.output(f'Credits\n\n            {2*self.sixteenth_note}{2*self.eighth_note}\n        {6*self.sixteenth_note}{6*self.eighth_note}\n      {8*self.sixteenth_note}{8*self.eighth_note}\n      {6*self.sixteenth_note}{4*char}{6*self.eighth_note}\n    {6*self.sixteenth_note}{8*char}{6*self.eighth_note}\n    {6*self.eighth_note}{8*char}{6*self.sixteenth_note}\n      {6*self.eighth_note}{4*char}{6*self.sixteenth_note}\n      {8*self.eighth_note}{8*self.sixteenth_note}\n        {6*self.eighth_note}{6*self.sixteenth_note}\n            {2*self.eighth_note}{2*self.sixteenth_note}\n\n                       Frums', wait_time)
        for _ in range(4):
            for _ in range(2):
                ender_pearl(self._uc('\xea'), False, self.half_beat_time)
                ender_pearl('.', False, self.half_beat_time)
                ender_pearl(self._uc('\xf7'), False, self.half_beat_time)
            for _ in range(2):
                ender_pearl(self._uc('\xea'), False, self.half_beat_time)
                ender_pearl('.', False, self.half_beat_time)
            ender_pearl(self._uc('\xf7'), False, self.half_beat_time)
            ender_pearl(self._uc('\xea'), True, self.half_beat_time)
            for _ in range(8):
                ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time)
                ender_pearl('.', True, self.half_quarter_beat_time)

    def _3(self):
        def ender_pearl(char:str, type:bool, wait_time:float, shine:int, text:bool):
            shine_char = self.light
            if shine == 1:
                shine_char = self.median
            elif shine == 2:
                shine_char = self.dark

            display_text = f"{self.smile} F" if text else "   "

            if type == False:
                self.output(f'Credits\n\n  {2*shine_char}        {2*self.eighth_note}{2*self.sixteenth_note}        {2*shine_char}\n {2*shine_char}     {6*self.eighth_note}{6*self.sixteenth_note}     {2*shine_char}\n {2*shine_char}   {8*self.eighth_note}{8*self.sixteenth_note}   {2*shine_char}\n{2*shine_char}    {6*self.eighth_note}{4*char}{6*self.sixteenth_note}    {2*shine_char}\n{2*shine_char}  {6*self.eighth_note}{8*char}{6*self.sixteenth_note}  {2*shine_char}\n{2*shine_char}  {6*self.sixteenth_note}{8*char}{6*self.eighth_note}  {2*shine_char}\n{2*shine_char}    {6*self.sixteenth_note}{4*char}{6*self.eighth_note}    {2*shine_char}\n {2*shine_char}   {8*self.sixteenth_note}{8*self.eighth_note}   {2*shine_char}\n {2*shine_char}     {6*self.sixteenth_note}{6*self.eighth_note}     {2*shine_char}\n  {2*shine_char}        {2*self.sixteenth_note}{2*self.eighth_note}        {2*shine_char}\n\n{display_text}                    Frums', wait_time)
            elif type == True:
                self.output(f'Credits\n\n  {2*shine_char}        {2*self.sixteenth_note}{2*self.eighth_note}        {2*shine_char}\n {2*shine_char}     {6*self.sixteenth_note}{6*self.eighth_note}     {2*shine_char}\n {2*shine_char}   {8*self.sixteenth_note}{8*self.eighth_note}   {2*shine_char}\n{2*shine_char}    {6*self.sixteenth_note}{4*char}{6*self.eighth_note}    {2*shine_char}\n{2*shine_char}  {6*self.sixteenth_note}{8*char}{6*self.eighth_note}  {2*shine_char}\n{2*shine_char}  {6*self.eighth_note}{8*char}{6*self.sixteenth_note}  {2*shine_char}\n{2*shine_char}    {6*self.eighth_note}{4*char}{6*self.sixteenth_note}    {2*shine_char}\n {2*shine_char}   {8*self.eighth_note}{8*self.sixteenth_note}   {2*shine_char}\n {2*shine_char}     {6*self.eighth_note}{6*self.sixteenth_note}     {2*shine_char}\n  {2*shine_char}        {2*self.eighth_note}{2*self.sixteenth_note}        {2*shine_char}\n\n{display_text}                    Frums', wait_time)

        for i in range(4):
            ender_pearl(self._uc('\xea'), False, self.half_quarter_beat_time/2, 2, False)
            ender_pearl(self._uc('\xea'), False, self.half_quarter_beat_time/2, 1, False)
            ender_pearl(self._uc('\xea'), False, self.half_quarter_beat_time, 0, False)
            ender_pearl('.', False, self.half_beat_time, 0, False)
            ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, False)
            ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, False)
            ender_pearl('.', False, self.half_quarter_beat_time/2, 2, False)
            ender_pearl('.', False, self.half_quarter_beat_time/2, 1, False)
            ender_pearl('.', False, self.half_quarter_beat_time, 0, False)
            ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, False)
            ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, False)
            ender_pearl('.', False, self.half_beat_time, 0, False)
            ender_pearl(self._uc('\xea'), False, self.half_quarter_beat_time/2, 2, False)
            ender_pearl(self._uc('\xea'), False, self.half_quarter_beat_time/2, 1, False)
            ender_pearl(self._uc('\xea'), False, self.half_quarter_beat_time, 0, False)
            ender_pearl('.', False, self.half_beat_time, 0, False)
            ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, False)
            ender_pearl(self._uc('\xea'), False, self.half_quarter_beat_time/2, 2, False)
            ender_pearl(self._uc('\xea'), False, self.half_quarter_beat_time/2, 1, False)
            ender_pearl(self._uc('\xea'), False, self.half_quarter_beat_time, 0, False)
            ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, False)
            ender_pearl('.', False, self.half_quarter_beat_time/2, 2, False)
            ender_pearl('.', False, self.half_quarter_beat_time/2, 1, False)
            ender_pearl('.', False, self.half_quarter_beat_time, 0, False)
            for _ in range(8):
                ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, True if i==3 else False)
                ender_pearl('.', True, self.half_quarter_beat_time, 0, False)

    def _4(self):
        thirteen_newlines = "\n" * 13 # 预先计算换行符字符串

        def ender_pearl(char:str, type:bool, wait_time:float, shine:int, text:str):
            shine_char = self.light
            if shine == 1:
                shine_char = self.median
            elif shine == 2:
                shine_char = self.dark

            display_text_line = f"{self.smile} {text if text else ''}"

            if not type:
                self.output(f'Credits\n\n  {2*shine_char}        {2*self.eighth_note}{2*self.sixteenth_note}        {2*shine_char}\n {2*shine_char}     {6*self.eighth_note}{6*self.sixteenth_note}     {2*shine_char}\n {2*shine_char}   {8*self.eighth_note}{8*self.sixteenth_note}   {2*shine_char}\n{2*shine_char}    {6*self.eighth_note}{4*char}{6*self.sixteenth_note}    {2*shine_char}\n{2*shine_char}  {6*self.eighth_note}{8*char}{6*self.sixteenth_note}  {2*shine_char}\n{2*shine_char}  {6*self.sixteenth_note}{8*char}{6*self.eighth_note}  {2*shine_char}\n{2*shine_char}    {6*self.sixteenth_note}{4*char}{6*self.eighth_note}    {2*shine_char}\n {2*shine_char}   {8*self.sixteenth_note}{8*self.eighth_note}   {2*shine_char}\n {2*shine_char}     {6*self.sixteenth_note}{6*self.eighth_note}     {2*shine_char}\n  {2*shine_char}        {2*self.sixteenth_note}{2*self.eighth_note}        {2*shine_char}\n\n{display_text_line}Frums', wait_time)
            else:
                self.output(f'Credits\n\n  {2*shine_char}        {2*self.sixteenth_note}{2*self.eighth_note}        {2*shine_char}\n {2*shine_char}     {6*self.sixteenth_note}{6*self.eighth_note}     {2*shine_char}\n {2*shine_char}   {8*self.sixteenth_note}{8*self.eighth_note}   {2*shine_char}\n{2*shine_char}    {6*self.sixteenth_note}{4*char}{6*self.eighth_note}    {2*shine_char}\n{2*shine_char}  {6*self.sixteenth_note}{8*char}{6*self.eighth_note}  {2*shine_char}\n{2*shine_char}  {6*self.eighth_note}{8*char}{6*self.sixteenth_note}  {2*shine_char}\n{2*shine_char}    {6*self.eighth_note}{4*char}{6*self.sixteenth_note}    {2*shine_char}\n {2*shine_char}   {8*self.eighth_note}{8*self.sixteenth_note}   {2*shine_char}\n {2*shine_char}     {6*self.eighth_note}{6*self.sixteenth_note}     {2*shine_char}\n  {2*shine_char}        {2*self.eighth_note}{2*self.sixteenth_note}        {2*shine_char}\n\n{display_text_line}Frums', wait_time)

        def shine(char:str, type:bool, text:str):
            ender_pearl(char, type, self.quarter_beat_time, 2, text)
            ender_pearl(char, type, self.half_quarter_beat_time, 1, text)
            ender_pearl(char, type, self.half_quarter_beat_time, 0, text)

        shine(self._uc('\xea'),False, 'Fun'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'Funding'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'Funding for'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'Funding for this'.ljust(21))
        shine(self._uc('\xf1'), False, 'pro'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'program'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'program was'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'program was made'.ljust(21))
        shine(self._uc('\xea'), False , 'po'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'possi'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'possible'.ljust(21))
        shine(self._uc('\xea'), True, 'possible by'.ljust(21))
        shine(self._uc('\xf1'), True, 'possible by (x2)'.ljust(21))
        ender_pearl(self._uc('\xf7'), True, self.half_beat_time, 0, 'possible by (x3)'.ljust(21))
        ender_pearl(self._uc('\xea'), True, self.half_beat_time, 0, 'possible by (x4)'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_beat_time, 0, 'possible by (x5)'.ljust(21))
        shine(self._uc('\xea'), False, 'Fun'.ljust(21))
        ender_pearl('.', False,self.quarter_beat_time, 2, 'possible by'.ljust(21))
        ender_pearl('.', False,self.quarter_beat_time, 0, 'possible by (x2)'.ljust(21))
        ender_pearl(self._uc('\xf7'), False,self.quarter_beat_time, 0, 'possible by (x3)'.ljust(21))
        ender_pearl(self._uc('\xf7'), False,self.quarter_beat_time, 0, 'possible by (x4)'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'Funding'.ljust(21))
        ender_pearl(self._uc('\xf1'), False, self.half_quarter_beat_time, 2, 'possible by'.ljust(21))
        ender_pearl(self._uc('\xf1'), False, self.half_quarter_beat_time, 0, 'possible by! (x2)'.ljust(21))
        ender_pearl(self._uc('\xf7'), False,self.quarter_beat_time, 0, 'possible by!! (x3)'.ljust(21))
        ender_pearl(self._uc('\xf7'), False,self.quarter_beat_time, 0, 'possible by!!! (x4)'.ljust(21))
        ender_pearl(self._uc('\xea'), False,self.half_beat_time, 0, 'Funding for'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for this'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thii'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thiii'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thiiii'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thiiiii'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thiiiiii'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thiiiiii'.ljust(21))
        shine(self._uc('\xea'), False, 'pro'.ljust(21))
        ender_pearl('.', False,self.half_beat_time, 0, 'program'.ljust(21))
        ender_pearl(self._uc('\xf7'), False,self.quarter_beat_time, 0, 'pro'.ljust(21))
        shine(self._uc('\xea'), True, 'program'.ljust(21))
        shine(self._uc('\xf1'), True, 'pro'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'pro (x2)'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'pro (x2)'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'pro (x3)'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'pro (x3)'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'pro (x4)'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'pro (x4)'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'pro'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'pro'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'progr'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'progr'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'progr'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'progr'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'program'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'program'.ljust(21))
        shine(self._uc('\xea'), False, 'Fun'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'Funding'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'Funding for'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'possible by'.ljust(21))
        shine(self._uc('\xf1'),  False, 'possible by (x2)'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'program was made'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'po'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'possi'.ljust(21))
        shine(self._uc('\xea'), False, 'possible by'.ljust(21))
        ender_pearl(self._uc('\xf1'), False, self.half_beat_time+self.quarter_beat_time, 0, 'view'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'viewers'.ljust(21))
        shine(self._uc('\xea'), True, 'viewers like'.ljust(21))
        shine(self._uc('\xf1'), True, 'viewers like you.'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))

        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'viewers like'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))
        shine(self._uc('\xea'), False, 'viewers like you'.ljust(21))

        ender_pearl('.', False, self.half_beat_time, 0, 'viewers like'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))

        shine(self._uc('\xf1'), True, 'viewers like'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))

        ender_pearl('.', False, self.half_beat_time, 0, 'viewers like'.ljust(21))
        shine(self._uc('\xea'), False, 'viewers like you.'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))

        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'viewers like'.ljust(21))
        shine(self._uc('\xea'), True, 'viewers like you.'.ljust(21))
        ender_pearl(self._uc('\xea'), True, self.half_quarter_beat_time, 0, 'viewers like you.'.ljust(21))

        ender_pearl('.', True, self.half_quarter_beat_time, 2, 'viewers like you.'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'viewers like you.'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'viewers like you.'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'viewers like you.'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'viewers like'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'viewers like'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'viewers like'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'viewers like'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'viewers like you.'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'viewers like you.'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'Fu'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'Fu (x2)'.ljust(21))

        shine(self._uc('\xea'),False, 'Fun'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'Funding'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'Funding for'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'Funding for this'.ljust(21))
        shine(self._uc('\xf1'), False, 'pro'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'program'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'program was'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'program was made'.ljust(21))
        shine(self._uc('\xea'), False , 'po'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'possi'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'possible'.ljust(21))
        shine(self._uc('\xea'), True, 'possible by'.ljust(21))
        shine(self._uc('\xf1'), True, 'possible by (x2)'.ljust(21))
        ender_pearl(self._uc('\xf7'), True, self.half_beat_time, 0, 'possible by (x3)'.ljust(21))
        ender_pearl(self._uc('\xea'), True, self.half_beat_time, 0, 'possible by (x4)'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_beat_time, 0, 'possible by (x5)'.ljust(21))
        shine(self._uc('\xea'), False, 'Fun'.ljust(21))
        ender_pearl('.', False,self.quarter_beat_time, 2, 'possible by'.ljust(21))
        ender_pearl('.', False,self.quarter_beat_time, 0, 'possible by (x2)'.ljust(21))
        ender_pearl(self._uc('\xf7'), False,self.quarter_beat_time, 0, 'possible by (x3)'.ljust(21))
        ender_pearl(self._uc('\xf7'), False,self.quarter_beat_time, 0, 'possible by (x4)'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'Funding'.ljust(21))
        ender_pearl(self._uc('\xf1'), False, self.half_quarter_beat_time, 2, 'possible by'.ljust(21))
        ender_pearl(self._uc('\xf1'), False, self.half_quarter_beat_time, 0, 'possible by! (x2)'.ljust(21))
        ender_pearl(self._uc('\xf7'), False,self.quarter_beat_time, 0, 'possible by!! (x3)'.ljust(21))
        ender_pearl(self._uc('\xf7'), False,self.quarter_beat_time, 0, 'possible by!!! (x4)'.ljust(21))
        ender_pearl(self._uc('\xea'), False,self.half_beat_time, 0, 'Funding for'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for this'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thii'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thiii'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thiiii'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thiiiii'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thiiiiii'.ljust(21))
        ender_pearl('.', False,self.half_quarter_beat_time, 0, 'Funding for thiiiiii'.ljust(21))
        shine(self._uc('\xea'), False, 'pro'.ljust(21))
        ender_pearl('.', False,self.quarter_beat_time, 0, 'program'.ljust(21))
        ender_pearl(self._uc('\xf7'), False,self.half_beat_time, 0, 'pro'.ljust(21))
        shine(self._uc('\xea'), True, 'program'.ljust(21))
        shine(self._uc('\xf1'), True, 'pro'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'pro (x2)'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'pro (x2)'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'pro (x3)'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'pro (x3)'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'pro (x4)'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'pro (x4)'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'pro'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'pro'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'progr'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'progr'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'progr'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'progr'.ljust(21))
        ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, 0, 'program'.ljust(21))
        ender_pearl('.', True, self.half_quarter_beat_time, 0, 'program'.ljust(21))
        shine(self._uc('\xea'), False, 'Fun'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'Funding'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'Funding for'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'possible by'.ljust(21))
        shine(self._uc('\xf1'),  False, 'possible by (x2)'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'program was made'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'po'.ljust(21))
        ender_pearl('.', False, self.half_beat_time+self.quarter_beat_time, 0, 'possi'.ljust(21))
        shine(self._uc('\xea'), False, 'possible by'.ljust(21))
        ender_pearl(self._uc('\xf1'), False, self.half_beat_time, 0, 'view'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'viewers'.ljust(21))
        shine(self._uc('\xea'), True, 'viewers like'.ljust(21))
        shine(self._uc('\xf1'), True, 'viewers like you.'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))

        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'viewers like'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))
        shine(self._uc('\xea'), False, 'viewers like you'.ljust(21))

        ender_pearl('.', False, self.half_beat_time, 0, 'viewers like'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))

        shine(self._uc('\xf1'), True, 'viewers like'.ljust(21))
        ender_pearl(self._uc('\xf7'), False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))
        ender_pearl(self._uc('\xea'), False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))

        ender_pearl('.', False, self.half_beat_time, 0, 'viewers like'.ljust(21))
        shine(self._uc('\xea'), False, 'viewers like you.'.ljust(21))
        ender_pearl('.', False, self.half_beat_time, 0, 'viewers like you.'.ljust(21))

        ender_pearl(self._uc('\xf1'), False, self.half_quarter_beat_time, 0, 'viewers like you.'.ljust(21))
        self.output(f'Credits\n\n  {self.light*2}{" "*20}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n {self.light*2}{" "*7}{self.eighth_note * 4}{self.sixteenth_note*4}{" "*7}{self.light*2}\n{self.light*2}{" "*6}{6*self.eighth_note}{6*self.sixteenth_note}{" "*6}{self.light*2}\n{self.light*2}{" "*6}{6*self.eighth_note}{6*self.sixteenth_note}{" "*6}{self.light*2}\n{self.light*2}{" "*6}{6*self.sixteenth_note}{6*self.eighth_note}{" "*6}{self.light*2}\n{self.light*2}{" "*6}{6*self.sixteenth_note}{6*self.eighth_note}{" "*6}{self.light*2}\n {self.light*2}{" "*7}{self.eighth_note * 4}{self.sixteenth_note*4}{" "*7}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n  {self.light*2}{" "*20}{self.light*2}\n\n{self.smile} viewers like you.    Frums', self.half_quarter_beat_time)
        self.output(f'Credits\n\n  {self.light*2}{" "*20}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n{self.light*2}{" "*10}{2*self.eighth_note}{2*self.sixteenth_note}{" "*10}{self.light*2}\n{self.light*2}{" "*8}{4*self.eighth_note}{4*self.sixteenth_note}{" "*8}{self.light*2}\n{self.light*2}{" "*8}{4*self.sixteenth_note}{4*self.eighth_note}{" "*8}{self.light*2}\n{self.light*2}{" "*10}{2*self.sixteenth_note}{2*self.eighth_note}{" "*10}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n  {self.light*2}{" "*20}{self.light*2}\n\n{self.smile} viewers like you.    Frums', self.half_quarter_beat_time)
        
        # 使用预计算的 thirteen_newlines
        self.output(f'Credits{thirteen_newlines}{self.smile} viewers like you.    Frums', self.quarter_beat_time + self.half_beat_time)
        self.output(f'Credits{thirteen_newlines}{(self.smile+" Broad").ljust(21)}  Frums', self.half_beat_time)
        self.output(f'Credits{thirteen_newlines}{(self.smile+" Broadcast").ljust(21)}  Frums', self.half_beat_time)


    def _5(self):
        thirteen_newlines = "\n" * 13 # 预先计算换行符字符串

        def _animate_box(shine:int, wait_time:float, type:bool, blocks:str, text:str):
            s = self.light if shine == 0 else (self.median if shine == 1 else self.dark)
            b = list(blocks.ljust(3, '.'))

            if(type == False):
                self.output(f'Credits\n\n   {s*2} {self._uc(0xc9)}{self._uc(0xcd)*4}{self._uc(0xbb)}       {self.eighth_note*2}   {s*2}\n  {s*2}  {self._uc(0xba)}{4*b[0]}{self._uc(0xba)}      {self.eighth_note*4}   {s*2}\n  {s*2}  {self._uc(0xba)}{4*b[0]}{self._uc(0xba)}       {self.eighth_note*2}    {s*2}\n {s*2}   {self._uc(0xc7)}{self._uc(0xc4)*4}{self._uc(0xb6)}      {self.eighth_note*4}    {s*2}\n {s*2}   {self._uc(0xba)}{4*b[1]}{self._uc(0xba)}     {self.eighth_note*6}   {s*2}\n {s*2}   {self._uc(0xba)}{4*b[1]}{self._uc(0xba)}     {self.eighth_note*6}   {s*2}\n {s*2}   {self._uc(0xc7)}{self._uc(0xc4)*4}{self._uc(0xb6)}     {self.eighth_note*6}   {s*2}\n  {s*2}  {self._uc(0xba)}{4*b[2]}{self._uc(0xba)}      {self.eighth_note*4}   {s*2}\n  {s*2}  {self._uc(0xba)}{4*b[2]}{self._uc(0xba)}      {self.eighth_note*4}   {s*2}\n   {s*2} {self._uc(0xc8)}{self._uc(0xcd)*4}{self._uc(0xbc)}     {self.eighth_note*2}  {self.eighth_note*2} {s*2}\n\n{self._uc(0xaf)} {text}Frums', wait_time)
            elif(type == True):
                self.output(f'Credits\n\n   {s*2} {self._uc(0xc9)}{self._uc(0xcd)*4}{self._uc(0xbb)}      {self.sixteenth_note*2}    {s*2}\n  {s*2}  {self._uc(0xba)}{4*b[0]}{self._uc(0xba)}     {self.sixteenth_note*4}    {s*2}\n  {s*2}  {self._uc(0xba)}{4*b[0]}{self._uc(0xba)}      {self.sixteenth_note*2}     {s*2}\n {s*2}   {self._uc(0xc7)}{self._uc(0xc4)*4}{self._uc(0xb6)}      {self.sixteenth_note*4}    {s*2}\n {s*2}   {self._uc(0xba)}{4*b[1]}{self._uc(0xba)}     {self.sixteenth_note*6}   {s*2}\n {s*2}   {self._uc(0xba)}{4*b[1]}{self._uc(0xba)}   {self.sixteenth_note*2} {self.sixteenth_note*4} {self.sixteenth_note*1}  {s*2}\n {s*2}   {self._uc(0xc7)}{self._uc(0xc4)*4}{self._uc(0xb6)}      {self.sixteenth_note*4}    {s*2}\n  {s*2}  {self._uc(0xba)}{4*b[2]}{self._uc(0xba)}     {self.sixteenth_note*2} {self.sixteenth_note*2}   {s*2}\n  {s*2}  {self._uc(0xba)}{4*b[2]}{self._uc(0xba)}    {self.sixteenth_note*2}  {self.sixteenth_note*2}   {s*2}\n   {s*2} {self._uc(0xc8)}{self._uc(0xcd)*4}{self._uc(0xbc)}    {self.sixteenth_note*2}   {self.sixteenth_note*2} {s*2}\n\n{self._uc(0xaf)} {text}Frums', wait_time)

        _animate_box(2, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Cor'.ljust(21))
        _animate_box(2, self.quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xf7')+'..', 'Corporation'.ljust(21))

        _animate_box(2, self.quarter_beat_time, False, '.'+self._uc('\xf1')+'.', 'Cor'.ljust(21))
        _animate_box(2, self.quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xf7')+'..', 'Corporation'.ljust(21))

        _animate_box(2, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Cor'.ljust(21))
        _animate_box(2, self.quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, '...', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, self._uc('\xf7')+'..', 'Corporation'.ljust(21))

        _animate_box(2, self.quarter_beat_time, True, '.'+self._uc('\xf1')+'.', 'Cor'.ljust(21))
        _animate_box(2, self.quarter_beat_time, True, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, self._uc('\xea')+'..', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, self._uc('\xea')+'..', 'Corpo'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '.'+self._uc('\xf1')+'.', 'Cor'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '...', 'Cor'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '.'+self._uc('\xf1')+'.', 'Cor (x2)'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '...', 'Cor (x2)'.ljust(21))
        _animate_box(2, self.half_quarter_beat_time, True, self._uc('\xea')+'..', 'Cor (x3)'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, '...', 'Cor (x3)'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corporation'.ljust(21))
        _animate_box(2, self.quarter_beat_time, False, '.'+self._uc('\xf1')+'.', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corporation'.ljust(21))
        _animate_box(2, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(2, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, '...', 'Corporation'.ljust(21))
        _animate_box(2, self.quarter_beat_time, True, '.'+self._uc('\xf1')+'.', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, '...', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, '..'+self._uc('\xf7'), 'Corporation'.ljust(21))
        _animate_box(2, self.quarter_beat_time, True, '.'+self._uc('\xea')+'.', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, '...', 'Corpo'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, '..'+self._uc('\xf7'), 'Corpo (x2)'.ljust(21))
        _animate_box(2, self.quarter_beat_time, True, self._uc('\xea')+'..', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, '...', 'Corpo'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, self._uc('\xea')+'..', 'Corpo (x2)'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '.'+self._uc('\xf1')+'.', 'Cor'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '...', 'Cor'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '.'+self._uc('\xf1')+'.', 'Corpo'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '...', 'Corpo'.ljust(21))

        _animate_box(2, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, '.'+self._uc('\xf7')+'.', 'Corpo'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'  ..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Cor (x2)'.ljust(21))
        _animate_box(2, self.quarter_beat_time, False, '.'+self._uc('\xf1')+'.', 'Cor (x3)'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Cor (x2)'.ljust(21))
        _animate_box(2, self.half_beat_time, False, self._uc('\xea')+'..', 'Cor (x3)'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corporation'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '..'+self._uc('\xf7'), 'Cor (x2)'.ljust(21))
        _animate_box(2, self.quarter_beat_time, True, '.'+self._uc('\xf1')+'.', 'Cor!'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '..'+self._uc('\xf7'), 'Corpor!'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, self._uc('\xea')+'..', 'Corpora!'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '...', 'Corpora!'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, self._uc('\xea')+'..', 'Corporation!'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, True, '...', 'Corporation!'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, '...', 'Cor!'.ljust(21))
        _animate_box(0, self.quarter_beat_time, True, '..'+self._uc('\xf7'), 'Cor! (x2)'.ljust(21))
        _animate_box(2, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Cor'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.half_quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Cor (x2)'.ljust(21))
        _animate_box(2, self.quarter_beat_time, False, '.'+self._uc('\xf1')+'.', 'Cor (x3)'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Cor (x2)'.ljust(21))
        _animate_box(2, self.quarter_beat_time, False, '.'+self._uc('\xf1')+'.', 'Cor (x3)'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Corpora'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corporation'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '...', 'Cor'.ljust(21))
        _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Cor (x2)'.ljust(21))
        for _ in range(4):
            _animate_box(2, self.quarter_beat_time, False, '.'+self._uc('\xf1')+'.', 'Cor'.ljust(21))
            _animate_box(0, self.quarter_beat_time, False, '..'+self._uc('\xf7'), 'Corpo'.ljust(21))
            _animate_box(0, self.quarter_beat_time, False, self._uc('\xea')+'..', 'Corpora'.ljust(21))
        
        # 使用预计算的 thirteen_newlines
        self.output(f'Credits{thirteen_newlines}{self._uc(0xaf)} {"Corporat".ljust(21)}Frums', self.half_quarter_beat_time)
        self.output(f'Credits{thirteen_newlines}{self._uc(0xaf)} {"Corporati".ljust(21)}Frums', self.half_quarter_beat_time)
        self.output(f'Credits{thirteen_newlines}{self._uc(0xaf)} {"Corporatio".ljust(21)}Frums', self.half_quarter_beat_time)
        self.output(f'Credits{thirteen_newlines}{self._uc(0xaf)} {"Corporation".ljust(21)}Frums', self.half_quarter_beat_time)
        self.output(f'Credits{thirteen_newlines}{self._uc(0xaf)} {"Corporation".ljust(21)}Frums', self.half_beat_time)


    def _6(self):
        cop = "Corporation"
        inv_cop = f"uo{chr(0x2c6)}{chr(0x2021)}{chr(0x2030)}{chr(0x2020)}od{chr(0x2020)}o{chr(0x2026)}"

        def _animate_complex_box(length:int, type:bool, block:list, shine:int, wait_time, repeat:int =1):
            s = self.light if shine == 0 else (self.median if shine == 1 else self.dark)
            r_char = self._uc(0xab) if repeat == 2 else self._uc(0xac) if repeat == 3 else ''
            
            b = list(block)
            while len(b) < 8:
                b.append(".......")

            top_text_prefix = f'{self._uc(0xa6)}x{r_char}{self._uc(0xa7)} ' if repeat != 1 else ''
            # Ensure length for inv_cop slicing is not negative
            slice_start = max(0, 11 - length)
            top_text = (top_text_prefix + inv_cop[slice_start:]).rjust(19)


            bottom_text_suffix = f' ({repeat}x)' if repeat != 1 else ''
            bottom_text = (cop[:length] + bottom_text_suffix).ljust(21)

            if(type==False):
                self.output(f'Credits{top_text} {self._uc(0xae)}\n\n   {s*2}{self._uc(0xc9)}{self._uc(0xcd)*9}{self._uc(0xd1)}{self._uc(0xcd)*7}{self._uc(0xbb)}{s*2}\n  {s*2} {self._uc(0xba)}         {self._uc(0x7c)}{b[0]}{self._uc(0xba)} {s*2}\n  {s*2} {self._uc(0xba)}   {self.eighth_note*2}    {self._uc(0x7c)}{b[1]}{self._uc(0xba)} {s*2}\n {s*2}  {self._uc(0xba)}  {self.eighth_note*4}   {self._uc(0x7c)}{b[2]}{self._uc(0xba)}  {s*2}\n {s*2}  {self._uc(0xba)}   {self.eighth_note*2}    {self._uc(0x7c)}{b[3]}{self._uc(0xba)}  {s*2}\n {s*2}  {self._uc(0xba)}  {self.eighth_note*4} {self.eighth_note} {self._uc(0x7c)}{b[4]}{self._uc(0xba)}  {s*2}\n {s*2}  {self._uc(0xba)} {self.eighth_note*6}  {self._uc(0x7c)}{b[5]}{self._uc(0xba)}  {s*2}\n  {s*2} {self._uc(0xba)} {self.eighth_note*5}   {self._uc(0x7c)}{b[6]}{self._uc(0xba)} {s*2}\n  {s*2} {self._uc(0xba)}{self._uc(0xdf)*9}{self._uc(0x7c)}{b[7]}{self._uc(0xba)} {s*2}\n   {s*2}{self._uc(0xc8)}{self._uc(0xcd)*9}{self._uc(0xcf)}{self._uc(0xcd)*7}{self._uc(0xbc)}{s*2}\n\n{self._uc(0xaf)} {bottom_text}Frums', wait_time)
            elif(type == True):
                self.output(f'Credits{top_text} {self._uc(0xae)}\n\n   {s*2}{self._uc(0xc9)}{self._uc(0xcd)*7}{self._uc(0xd1)}{self._uc(0xcd)*9}{self._uc(0xbb)}{s*2}\n  {s*2} {self._uc(0xba)}{b[0]}{self._uc(0x7c)}         {self._uc(0xba)} {s*2}\n  {s*2} {self._uc(0xba)}{b[1]}{self._uc(0x7c)}    {self.sixteenth_note*2}   {self._uc(0xba)} {s*2}\n {s*2}  {self._uc(0xba)}{b[2]}{self._uc(0x7c)}   {self.sixteenth_note*4}  {self._uc(0xba)}  {s*2}\n {s*2}  {self._uc(0xba)}{b[3]}{self._uc(0x7c)}    {self.sixteenth_note*2}   {self._uc(0xba)}  {s*2}\n {s*2}  {self._uc(0xba)}{b[4]}{self._uc(0x7c)} {self.sixteenth_note} {self.sixteenth_note*4}  {self._uc(0xba)}  {s*2}\n {s*2}  {self._uc(0xba)}{b[5]}{self._uc(0x7c)}  {self.sixteenth_note*6} {self._uc(0xba)}  {s*2}\n  {s*2} {self._uc(0xba)}{b[6]}{self._uc(0x7c)}   {self.sixteenth_note*5} {self._uc(0xba)} {s*2}\n  {s*2} {self._uc(0xba)}{b[7]}{self._uc(0x7c)}{self._uc(0xdf)*9}{self._uc(0xba)} {s*2}\n   {s*2}{self._uc(0xc8)}{self._uc(0xcd)*7}{self._uc(0xcf)}{self._uc(0xcd)*9}{self._uc(0xbc)}{s*2}\n\n{self._uc(0xaf)} {bottom_text}Frums', wait_time)

        kick_blocks = ['..'+self._uc('\xea')*3+'..', '.'+self._uc('\xea')+'...'+self._uc('\xea')+'.', self._uc('\xea')+'.....'+self._uc('\xea'), self._uc('\xea')+'.....'+self._uc('\xea'), '.'+self._uc('\xea')+'...'+self._uc('\xea')+'.', '.'+self._uc('\xea')+'...'+self._uc('\xea')+'.', self._uc('\xea')*2+'...'+self._uc('\xea')*2, 'K i c k']
        none_blocks = ['.......' if x!=7 else 'N o n e' for x in range(8) ]
        ride_blocks = ['.......', '.'+self._uc('\xf7')*3+'.'+self._uc('\xf7')*2, self._uc('\xf7')*2+'.'+self._uc('\xf7')*3+'.', '.......', '.'+self._uc('\xf7')*3+'.'+self._uc('\xf7')*2, self._uc('\xf7')*2+'.'+self._uc('\xf7')*3+'.', '.......', 'R i d e']
        shot_blocks = ['...'+self._uc('\xf1')+'...' if x!=2 and x!=7 else ('.'+self._uc('\xf1')*5+'.' if x==2 or x==6 else 'S h o t' ) for x in range(8)]


        for i in range(4):
            _animate_complex_box(3, False, kick_blocks, 2, self.half_quarter_beat_time, 3 if i != 0 else 1)
            _animate_complex_box(3, False, kick_blocks, 0, self.half_quarter_beat_time, 3 if i != 0 else 1)
            _animate_complex_box(5, False, none_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(7, False, ride_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(3, False, kick_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(5, False, none_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(3, False, kick_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(5, False, none_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(7, False, ride_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(3, False, shot_blocks, 2, self.half_quarter_beat_time)
            _animate_complex_box(3, False, shot_blocks, 0, self.half_quarter_beat_time)
            _animate_complex_box(5, False, none_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(7, False, ride_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(3, False, kick_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(5, False, none_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(3, False, kick_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(5, False, none_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(3, False, kick_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(5, False, none_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(7, False, ride_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(3, False, kick_blocks, 2, self.half_quarter_beat_time)
            _animate_complex_box(3, False, kick_blocks, 0, self.half_quarter_beat_time)
            _animate_complex_box(5, False, none_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(7, False, ride_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(3, False, kick_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(5, False, none_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(3, False, kick_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(5, True, none_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(7, True, ride_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(3, True, shot_blocks, 2, self.half_quarter_beat_time)
            _animate_complex_box(3, True, shot_blocks, 0, self.half_quarter_beat_time)
            _animate_complex_box(5, True, none_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(7, True, ride_blocks, 0, self.quarter_beat_time)
            _animate_complex_box(3, True, shot_blocks, 2, self.half_quarter_beat_time)
            _animate_complex_box(3, True, shot_blocks, 0, self.half_quarter_beat_time)
            if(i==3):break
            _animate_complex_box(3, True, shot_blocks, 2, self.half_quarter_beat_time, 2)
            _animate_complex_box(3, True, shot_blocks, 0, self.half_quarter_beat_time, 2)

    def _7(self):
        inv_tion = f"uo{chr(0x2c6)}{chr(0x2021)}"
        inv_cop = f"uo{chr(0x2c6)}{chr(0x2021)}{chr(0x2030)}{chr(0x2020)}od{chr(0x2020)}o{chr(0x2026)}"
        cop = "Corporation"

        def ender_pearl(char:str, type:bool, wait_time:float, text:list, shine:int =0, hide:bool =False):
            s = self.light if shine == 0 else (self.median if shine == 1 else self.dark)
            
            text_list = list(text)
            while len(text_list) < 2:
                text_list.append("".ljust(21))

            top_line_text = text_list[0]
            bottom_line_text = text_list[1]

            ae_char = self._uc(0xae) if not hide else ' '
            af_char = self._uc(0xaf) if not hide else ' '


            if type == False:
                self.output(f'Credits{top_line_text}{ae_char}\n\n  {s*2}        {2*self.eighth_note}{2*self.sixteenth_note}        {s*2}\n {s*2}      {6*self.eighth_note}{6*self.sixteenth_note}    {s*2}\n {s*2}   {8*self.eighth_note}{8*self.sixteenth_note}   {s*2}\n{s*2}    {6*self.eighth_note}{4*char}{6*self.sixteenth_note}    {s*2}\n{s*2}  {6*self.eighth_note}{8*char}{6*self.sixteenth_note}  {s*2}\n{s*2}  {6*self.sixteenth_note}{8*char}{6*self.eighth_note}  {s*2}\n{s*2}    {6*self.sixteenth_note}{4*char}{6*self.eighth_note}    {s*2}\n {s*2}   {8*self.sixteenth_note}{8*self.eighth_note}   {s*2}\n {s*2}     {6*self.sixteenth_note}{6*self.eighth_note}     {s*2}\n  {s*2}        {2*self.sixteenth_note}{2*self.eighth_note}        {s*2}\n\n{af_char}{bottom_line_text}Frums', wait_time)
            elif type == True:
                self.output(f'Credits{top_line_text}{ae_char}\n\n  {s*2}        {2*self.sixteenth_note}{2*self.eighth_note}        {s*2}\n {s*2}      {6*self.sixteenth_note}{6*self.eighth_note}    {s*2}\n {s*2}   {8*self.sixteenth_note}{8*self.eighth_note}   {s*2}\n{s*2}    {6*self.sixteenth_note}{4*char}{6*self.eighth_note}    {s*2}\n{s*2}  {6*self.sixteenth_note}{8*char}{6*self.eighth_note}  {s*2}\n{s*2}  {6*self.eighth_note}{8*char}{6*self.sixteenth_note}  {s*2}\n{s*2}    {6*self.eighth_note}{4*char}{6*self.sixteenth_note}    {s*2}\n {s*2}   {8*self.eighth_note}{8*self.sixteenth_note}   {s*2}\n {s*2}     {6*self.eighth_note}{6*self.sixteenth_note}     {s*2}\n  {s*2}        {2*self.eighth_note}{2*self.sixteenth_note}        {s*2}\n\n{af_char}{bottom_line_text}Frums', wait_time)

        dagger_char = chr(0x2021)
        ae_char_static = self._uc(0xae)
        af_char_static = self._uc(0xaf)
        
        # Note: The f-string `f'Credits{top_dynamic_text} {ae_char_static}{"\n"*13}{af_char_static} ...'`
        # is correct because "\n"*13 is a literal part of the f-string, not inside an expression `{}`.
        # What a sh*t problem......
        thirteen_newlines_literal = "\n" * 13


        for i in range(12):
            slice_end = max(0, len(inv_cop) -3) # Ensure slice is valid
            top_dynamic_text = (i * dagger_char).rjust(11) + inv_cop[3:slice_end if slice_end > 3 else len(inv_cop)] # Adjusted slicing
            bottom_dynamic_text = (cop[:8] + i * 't').ljust(21)
            self.output(f'Credits{top_dynamic_text} {ae_char_static}{thirteen_newlines_literal}{af_char_static} {bottom_dynamic_text}Frums', self.half_quarter_beat_time/2)
            if(i==7):
                top_dynamic_text_shine = (i * dagger_char).rjust(11) + inv_cop[3:slice_end if slice_end > 3 else len(inv_cop)] + self.light
                bottom_dynamic_text_shine = (self.light + cop[:8] + i * 't').ljust(22)
                self.output(f'Credits{top_dynamic_text_shine}{ae_char_static}{thirteen_newlines_literal}{af_char_static}{bottom_dynamic_text_shine}Frums', self.half_quarter_beat_time/2)
            if(i==8):
                slice_end_shine = max(0, len(inv_cop) -1)
                top_dynamic_text_shine = (i * dagger_char).rjust(11) + inv_cop[3:slice_end_shine if slice_end_shine > 3 else len(inv_cop)] + self.light*2
                bottom_dynamic_text_shine = (self.light*2 + cop[1:8] + i * 't').ljust(23)
                self.output(f'Credits{top_dynamic_text_shine}{ae_char_static}{thirteen_newlines_literal}{af_char_static}{bottom_dynamic_text_shine}Frums', self.half_quarter_beat_time/2)

        top_final_text = (12 * dagger_char).rjust(13) + self.light*7
        bottom_final_text = (self.light*7 + 12*'t').ljust(26)
        self.output(f'Credits{top_final_text}{ae_char_static}{thirteen_newlines_literal}{af_char_static}{bottom_final_text}Frums', self.half_quarter_beat_time/2)

        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(inv_tion + self.dark*8).rjust(20)}', f'{self.dark*8}tion'.ljust(22)], shine=2)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(self.median*8).rjust(20)}', f'{self.median*8}'.ljust(22)], hide=True, shine=1)
        ender_pearl('.', False, self.quarter_beat_time, [f'{(inv_tion + self.light*8).rjust(20)}', f'{self.light*8}tion'.ljust(22)])
        ender_pearl('.', False, self.quarter_beat_time, [f'{(self.median*8).rjust(20)}', f'{self.median*8}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{(inv_tion + self.dark*8).rjust(20)}', f'{self.dark*8}tion'.ljust(22)], shine=0) # shine was unspecified, assuming 0 or 2 based on pattern
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{(self.median*8).rjust(20)}', f'{self.median*8}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(inv_tion + self.light*8).rjust(20)}', f'{self.light*8}tion'.ljust(22)])
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(self.median*8).rjust(20)}', f'{self.median*8}'.ljust(22)], hide=True)
        ender_pearl('.', False, self.quarter_beat_time, [f'{(inv_tion+" " + self.dark*7).rjust(20)}', f'{self.dark*7} tion'.ljust(22)], shine=2)
        ender_pearl('.', False, self.quarter_beat_time, [f'{(self.median*7).rjust(20)}', f'{self.median*7}'.ljust(22)], hide=True, shine=1)
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{(inv_tion+" "  + self.light*7).rjust(20)}', f'{self.light*7} tion'.ljust(22)])
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{(self.median*7).rjust(20)}', f'{self.median*7}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(inv_tion+" "  + self.dark*7).rjust(20)}', f'{self.dark*7} tion'.ljust(22)], shine=0)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(self.median*7).rjust(20)}', f'{self.median*7}'.ljust(22)], hide=True)
        ender_pearl('.', False, self.quarter_beat_time, [f'{(inv_tion+" "  + self.light*7).rjust(20)}', f'{self.light*7} tion'.ljust(22)])
        ender_pearl('.', False, self.quarter_beat_time, [f'{(self.median*7).rjust(20)}', f'{self.median*7}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(inv_tion[:3]+"   "+self.dark*6).rjust(20)}', f'{self.dark*6}   ion'.ljust(22)], shine=2)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(self.median*6).rjust(20)}', f'{self.median*6}'.ljust(22)], hide=True, shine=1)
        ender_pearl('.', False, self.quarter_beat_time, [f'{(inv_tion[:3]+"   "+self.light*6).rjust(20)}', f'{self.light*6}   ion'.ljust(22)])
        ender_pearl('.', False, self.quarter_beat_time, [f'{(self.median*6).rjust(20)}', f'{self.median*6}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{(inv_tion[:3]+"   "+self.dark*6).rjust(20)}', f'{self.dark*6}   ion'.ljust(22)], shine=0)
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{(self.median*6).rjust(20)}', f'{self.median*6}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xea'), True, self.quarter_beat_time, [f'{(inv_tion[:3]+"   "+self.light*6).rjust(20)}', f'{self.light*6}   ion'.ljust(22)], shine=2)
        ender_pearl(self._uc('\xea'), True, self.quarter_beat_time, [f'{(self.median*6).rjust(20)}', f'{self.median*6}'.ljust(22)], hide=True, shine=1)
        for i in range(8):
            ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, [f'{(inv_tion[:3]+"    "+self.light*5).rjust(20)}', f'{self.light*5}    ion'.ljust(22)] if i%2==0 else [f'{(self.median*5).rjust(20)}', f'{self.median*5}'.ljust(22)], shine=2 if i==0 else 0)
            ender_pearl('.', True, self.half_quarter_beat_time, [f'{(self.median*5).rjust(20)}', f'{self.median*5}'.ljust(22)] if i%2 == 0 else [f'{(inv_tion[:3]+"    "+self.light*5).rjust(20)}', f'{self.light*5}    ion'.ljust(22)], hide=True, shine=1 if i==0 else 0)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{("uo"+ " "*6 + self.dark*4).rjust(20)}', f'{self.dark*4}      on'.ljust(22)], shine=2)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(self.median*4).rjust(20)}', f'{self.median*4}'.ljust(22)], hide=True, shine=1)
        ender_pearl('.', False, self.quarter_beat_time, [f'{("uo"+ " "*6 + self.light*4).rjust(20)}', f'{self.light*4}      on'.ljust(22)])
        ender_pearl('.', False, self.quarter_beat_time, [f'{(self.median*4).rjust(20)}', f'{self.median*4}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{("uo"+ " "*6 + self.dark*4).rjust(20)}', f'{self.dark*4}      on'.ljust(22)], shine=0)
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{(self.median*4).rjust(20)}', f'{self.median*4}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{("uo"+ " "*6 + self.light*4).rjust(20)}', f'{self.light*4}      on'.ljust(22)])
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(self.median*4).rjust(20)}', f'{self.median*4}'.ljust(22)], hide=True)
        ender_pearl('.', False, self.quarter_beat_time, [f'{("uo"+" "*7 + self.dark*3).rjust(20)}', f'{self.dark*3}       on'.ljust(22)], shine=2)
        ender_pearl('.', False, self.quarter_beat_time, [f'{(self.median*3).rjust(20)}', f'{self.median*3}'.ljust(22)], hide=True, shine=1)
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{("uo"+" "*7  + self.light*3).rjust(20)}', f'{self.light*3}       on'.ljust(22)])
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{(self.median*3).rjust(20)}', f'{self.median*3}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{("uo"+" "*7  + self.dark*3).rjust(20)}', f'{self.dark*3}       on'.ljust(22)], shine=0)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(self.median*3).rjust(20)}', f'{self.median*3}'.ljust(22)], hide=True)
        ender_pearl('.', False, self.quarter_beat_time, [f'{("uo"+" "*7  + self.light*3).rjust(20)}', f'{self.light*3}       on'.ljust(22)])
        ender_pearl('.', False, self.quarter_beat_time, [f'{(self.median*3).rjust(20)}', f'{self.median*3}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{("u         "+self.dark*2).rjust(20)}', f'{self.dark*2}         n'.ljust(22)], shine=2)
        ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, [f'{(self.median*2).rjust(20)}', f'{self.median*2}'.ljust(22)], hide=True, shine=1)
        ender_pearl('.', False, self.quarter_beat_time,  [f'{("u         "+self.light*2).rjust(20)}', f'{self.light*2}         n'.ljust(22)])
        ender_pearl('.', False, self.quarter_beat_time, [f'{(self.median*2).rjust(20)}', f'{self.median*2}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{("u         "+self.dark*2).rjust(20)}', f'{self.dark*2}         n'.ljust(22)], shine=0)
        ender_pearl(self._uc('\xf7'), False, self.quarter_beat_time, [f'{(self.median*2).rjust(20)}', f'{self.median*2}'.ljust(22)], hide=True)
        ender_pearl(self._uc('\xea'), True, self.quarter_beat_time, [f'{("u         "+self.light*2).rjust(20)}', f'{self.light*2}         n'.ljust(22)], shine=2)
        ender_pearl(self._uc('\xea'), True, self.quarter_beat_time, [f'{(self.median*2).rjust(20)}', f'{self.median*2}'.ljust(22)], hide=True, shine=1)
        for i in range(8):
            ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time, [f'{("u          "+self.light).rjust(20)}', f'{self.light}          n'.ljust(22)] if i%2==0 else [f'{(self.median).rjust(20)}', f'{self.median}'.ljust(22)], shine=2 if i==0 else 0)
            ender_pearl('.', True, self.half_quarter_beat_time, [f'{(self.median).rjust(20)}', f'{self.median}'.ljust(22)] if i%2 == 0 else [f'{("u          "+self.light).rjust(20)}', f'{self.light}          n'.ljust(22)], hide=True, shine=1 if i==0 else 0)

    def _8(self):
        def ender_pearl(char:str, type:bool, wait_time:float, shine:int = 0):
            s_char = self.light
            if shine == 1:
                s_char = self.median
            elif shine == 2:
                s_char = self.dark

            if type == False:
                self.output(f'Credits\n\n  {2*s_char}        {2*self.eighth_note}{2*self.sixteenth_note}        {2*s_char}\n {2*s_char}     {6*self.eighth_note}{6*self.sixteenth_note}     {2*s_char}\n {2*s_char}   {8*self.eighth_note}{8*self.sixteenth_note}   {2*s_char}\n{2*s_char}    {6*self.eighth_note}{4*char}{6*self.sixteenth_note}    {2*s_char}\n{2*s_char}  {6*self.eighth_note}{8*char}{6*self.sixteenth_note}  {2*s_char}\n{2*s_char}  {6*self.sixteenth_note}{8*char}{6*self.eighth_note}  {2*s_char}\n{2*s_char}    {6*self.sixteenth_note}{4*char}{6*self.eighth_note}    {2*s_char}\n {2*s_char}   {8*self.sixteenth_note}{8*self.eighth_note}   {2*s_char}\n {2*s_char}     {6*self.sixteenth_note}{6*self.eighth_note}     {2*s_char}\n  {2*s_char}        {2*self.sixteenth_note}{2*self.eighth_note}        {2*s_char}\n\n                       Frums', wait_time)
            elif type == True:
                self.output(f'Credits\n\n  {2*s_char}        {2*self.sixteenth_note}{2*self.eighth_note}        {2*s_char}\n {2*s_char}     {6*self.sixteenth_note}{6*self.eighth_note}     {2*s_char}\n {2*s_char}   {8*self.sixteenth_note}{8*self.eighth_note}   {2*s_char}\n{2*s_char}    {6*self.sixteenth_note}{4*char}{6*self.eighth_note}    {2*s_char}\n{2*s_char}  {6*self.sixteenth_note}{8*char}{6*self.eighth_note}  {2*s_char}\n{2*s_char}  {6*self.eighth_note}{8*char}{6*self.sixteenth_note}  {2*s_char}\n{2*s_char}    {6*self.eighth_note}{4*char}{6*self.sixteenth_note}    {2*s_char}\n {2*s_char}   {8*self.eighth_note}{8*self.sixteenth_note}   {2*s_char}\n {2*s_char}     {6*self.eighth_note}{6*self.sixteenth_note}     {2*s_char}\n  {2*s_char}        {2*self.eighth_note}{2*self.sixteenth_note}        {2*s_char}\n\n                       Frums', wait_time)

        for i in range(6):
            ender_pearl(self._uc('\xea'), False, self.quarter_beat_time,2)
            ender_pearl(self._uc('\xea'), False, self.quarter_beat_time,1)
            ender_pearl('.', False, self.half_beat_time)
            ender_pearl(self._uc('\xf7'), False, self.half_beat_time)
            ender_pearl(self._uc('\xea'), False, self.half_beat_time)
            ender_pearl('.', False, self.quarter_beat_time, 2)
            ender_pearl('.', False, self.quarter_beat_time, 1)
            ender_pearl(self._uc('\xf7'), False, self.half_beat_time)
            ender_pearl(self._uc('\xea'), False, self.half_beat_time)
            ender_pearl('.', False, self.half_beat_time)
            ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, 2)
            ender_pearl(self._uc('\xea'), False, self.quarter_beat_time, 2)
            ender_pearl('.', False, self.half_beat_time)
            ender_pearl(self._uc('\xf7'), False, self.half_beat_time)
            ender_pearl(self._uc('\xea'), True, self.quarter_beat_time, 2)
            ender_pearl(self._uc('\xea'), True, self.quarter_beat_time, 1)
            if(i==5):break
            for k in range(8):
                ender_pearl(self._uc('\xf1'), True, self.half_quarter_beat_time,2 if k==0 else 0)
                ender_pearl('.', True, self.half_quarter_beat_time)

        ender_pearl(self._uc('\xf1'), False, self.half_quarter_beat_time, 0)
        self.output(f'Credits\n\n  {self.light*2}{" "*20}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n {self.light*2}{" "*7}{self.eighth_note * 4}{self.sixteenth_note*4}{" "*7}{self.light*2}\n{self.light*2}{" "*6}{6*self.eighth_note}{6*self.sixteenth_note}{" "*6}{self.light*2}\n{self.light*2}{" "*6}{6*self.eighth_note}{6*self.sixteenth_note}{" "*6}{self.light*2}\n{self.light*2}{" "*6}{6*self.sixteenth_note}{6*self.eighth_note}{" "*6}{self.light*2}\n{self.light*2}{" "*6}{6*self.sixteenth_note}{6*self.eighth_note}{" "*6}{self.light*2}\n {self.light*2}{" "*7}{self.eighth_note * 4}{self.sixteenth_note*4}{" "*7}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n  {self.light*2}{" "*20}{self.light*2}\n\n                       Frums', self.half_quarter_beat_time)
        self.output(f'Credits\n\n  {self.light*2}{" "*20}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n{self.light*2}{" "*10}{2*self.eighth_note}{2*self.sixteenth_note}{" "*10}{self.light*2}\n{self.light*2}{" "*8}{4*self.eighth_note}{4*self.sixteenth_note}{" "*8}{self.light*2}\n{self.light*2}{" "*8}{4*self.sixteenth_note}{4*self.eighth_note}{" "*8}{self.light*2}\n{self.light*2}{" "*10}{2*self.sixteenth_note}{2*self.eighth_note}{" "*10}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n {self.light*2}{" "*22}{self.light*2}\n  {self.light*2}{" "*20}{self.light*2}\n\n                       Frums', self.half_quarter_beat_time)
        
        thirteen_newlines = "\n" * 13 # 定义在这里，因为 _8 的最后一行也用到了
        self.output(f'Credits{thirteen_newlines}                       Frums', self.quarter_beat_time + self.half_beat_time)
        time.sleep(self.half_beat_time)
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')


if __name__ == '__main__':
    try:
        Credits_BGA()
    except KeyboardInterrupt:
        print("\n用户中断了程序。正在退出...") # 防止output变成一坨
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        print('\x1b[?25h', end='')
        sys.stdout.flush()
    except Exception as e:
        print(f"\n意外错误: {e}")
        import traceback
        traceback.print_exc()
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        print('\x1b[?25h', end='')
        sys.stdout.flush()

