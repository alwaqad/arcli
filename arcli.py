#!/usr/bin/env python3
######################################
#.......#.....................#...#..#
#.......#.....................#...#..#
#.......#.......#.#...........#...#..#
#.#####.#.......###.####......#...#..#
#.....#.#.......#.#.#..#......#...#..#
#.#####.###########.###########...#..#
#......................#.............#
#...................###..............#
#....................................#
######################################

#

###################################################
#.................................................#
#.......................V.........................#
#..V....................V.........................#
#..V....................V.....................V...#
#..V............V..V....V...........VVVV.....VVV..#
#..V.....V.V.V......V...V...........V..V.....V.V..#
#..VVVVVVVVVVVVVVVVVV...V.......V...VVVVVVVVVVVV..#
#..............................V.......V..........#
#.............................V.....VVV...........#
#..........................VVV....................#
###################################################

#

    ###         ####           ####
 #  #           #  #           #
 #  ###     #   ###################
 #    #    #       #    # #
 ######   #     ###     ###
  #  # ###

#

## https://github.com/alwaqad/arcli

import os
import sys

## دالة للبحث عن ملف الخط في عدة مواقع
def find_font_file(fontname):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(script_dir, f"{fontname}.txt")
    if os.path.exists(local_path):
        return local_path

    user_path = os.path.expanduser(f"~/.local/share/arcli/{fontname}.txt")
    if os.path.exists(user_path):
        return user_path

    system_path = f"/usr/local/share/arcli/{fontname}.txt"
    if os.path.exists(system_path):
        return system_path

    old_system_path = f"/usr/share/arcli/{fontname}.txt"
    if os.path.exists(old_system_path):
        return old_system_path

    current_dir = f"{fontname}.txt"
    if os.path.exists(current_dir):
        return current_dir

    return None

## دالة تتأكد أن الحرف من الحروف المتصلة أو المنفصلة
def is_connectable(letter):
    if (letter[0] == 'ا' or letter[0] == 'أ' or letter[0] == 'إ' or letter[0] == 'آ'):
        return False
    elif (letter[0] == 'د'):
        return False
    elif (letter[0] == 'ذ'):
        return False
    elif (letter[0] == 'ر'):
        return False
    elif (letter[0] == 'ز'):
        return False
    elif (letter[0] == 'و'):
        return False
    elif (letter[0] == 'ء'):
        return False
    elif (letter[0] == ' '):
        return False
    else:
        return True

## دالة تتأكد أن الحرف ضمن الحروف العربية المدعومة، والمسافة
def is_arabic(word):
    arabic_letters = {
        'ا', 'أ', 'آ', 'إ', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ',
        'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ',
        'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'ة',
        'و', 'ؤ', 'ي', 'ى', 'ئ', 'ء', ' '
    }

    for letter in word:
        if letter not in arabic_letters:
            return False
    return True

## دالة تتأكد من موضع كل حرف في الكلمة وتسمي كل حرف في القائمة بالملحق المناسب له
def letters_locations(word):
    words = word.split()
    all_letters = []

    for word in words:
        if not word:
            continue

        numberedword = list(word)
        word_length = len(word)

        if (word_length>1):
            for i in range(word_length):
                if (word[i] == " "):
                    numberedword[i]="مسافة"
                else:
                    if (i == 0):
                        if (is_connectable(numberedword[i])):
                            all_letters.append(numberedword[i]+"_مبتدأ")
                        else:
                            all_letters.append(numberedword[i]+"_وحيد")
                    elif (i == (word_length-1)):
                        if (is_connectable(word[i-1])):
                            all_letters.append(numberedword[i]+"_منتهى")
                        else:
                            all_letters.append(numberedword[i]+"_وحيد")
                    else:
                        if (is_connectable(numberedword[i])):
                            if (is_connectable(word[i-1])):
                                all_letters.append(numberedword[i]+"_وسط")
                            else:
                                all_letters.append(numberedword[i]+"_مبتدأ")
                        else:
                            if (is_connectable(word[i-1])):
                                all_letters.append(numberedword[i]+"_وسط")
                            else:
                                all_letters.append(numberedword[i]+"_وحيد")
        else:
            all_letters.append(numberedword[0]+"_وحيد")

        if word != words[-1]:
            all_letters.append("مسافة")

    return all_letters

## دالة تحويل اسم اللون إلى رمزه
def get_color_code(color):
    if color is None:
        return ''
    colors = {
        'white': '\033[97m',
        'grey': '\033[90m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'pink': '\033[95m',
        'magenta': '\033[95m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'reset': '\033[0m'
    }
    return colors.get(color.lower(), '')

## دالة تمر على الأسطر في ملف الخط وتضيف الأحرف في قائمة ثم تطبعها
def printletters(lettersarray, fontname, color=None, no_dots=False):
    fontpath = find_font_file(fontname)
    if fontpath is None:
        print(f"خطأ: ملف الخط {fontname} غير موجود")
        return

    try:
        with open(fontpath, 'r', encoding='utf-8') as font:
            fontlines = font.readlines()
    except FileNotFoundError:
        print(f"خطأ: ملف الخط {fontname} غير موجود")
        return
    except Exception as e:
        print(f"خطأ في قراءة ملف الخط: {e}")
        return

    startlines = []
    x=0
    for letter in lettersarray:
        for linenumber, line in enumerate(fontlines):
            if (lettersarray[x] in line):
                startlines.append([])
                for i in range(1,11,1):
                    font_line = fontlines[linenumber+i]
                    if no_dots:
                        font_line = font_line.replace('.', ' ')
                    startlines[x].append(font_line)
                x+=1
                break

    color_code = get_color_code(color)
    reset_code = '\033[0m' if color else ''

    for line in range(10):
        for letter in reversed(startlines):
            printnow = letter[line]
            if color:
                print(f"{color_code}{printnow[:-1]}{reset_code}", end='')
            else:
                print(printnow[:-1], end='')
        print()

## الحصول على المدخلات من المستخدم
font_choice = "font1"
color_choice = None
no_dots = False

## معالجة وسائط سطر الأوامر
args = sys.argv[1:]
i = 0
while i < len(args):
    if args[i] in ["font1", "font2", "font3", "font4", "font5", "font6"]:
        font_choice = args[i]
    elif args[i] in ["--color", "-c"] and i + 1 < len(args):
        color_choice = args[i + 1]
        i += 1
    elif args[i] in ["--no-dots", "-nd"]:
        no_dots = True
    elif args[i] in ["--help", "-h"]:
        print("الاستخدام:")
        print("  ./arcli.py [خيارات] [نص]")
        print("الخيارات:")
        print("  font1-font6        اختيار الخط")
        print("  --color, -c [لون]  اختيار اللون (white, grey, red, green, yellow, blue, pink, magenta, purple, cyan)")
        print("  --no-dots, -nd استبدال النقاط بمسافات")
        print("  --help, -h         عرض المساعدة")
        sys.exit(0)
    i += 1

## تحديد النص المدخل من المستخدم
if any(arg in sys.argv for arg in ["--color", "-c", "--no-dots", "-nd", "--help", "-h"]):
    non_option_args = [arg for arg in args if not arg.startswith('-') and arg not in ["font1", "font2", "font3", "font4", "font5", "font6"] and arg not in ["white", "grey", "red", "green", "yellow", "blue", "pink", "magenta", "purple", "cyan"]]
    if non_option_args:
        word = ' '.join(non_option_args)
    else:
        word = input("اكتب كلمتك: ")
else:
    if len(sys.argv) > 1:
        if sys.argv[1] in ["font1", "font2", "font3", "font4", "font5", "font6"]:
            font_choice = sys.argv[1]
            if len(sys.argv) > 2:
                word = ' '.join(sys.argv[2:])
            else:
                word = input("اكتب كلمتك: ")
        else:
            word = ' '.join(sys.argv[1:])
    else:
        print("الخطوط المتاحة: font1, font2, font3, font4, font5, font6")
        font_input = input("اختر الخط (افتراضي: font1): ").strip()
        if font_input in ["font1", "font2", "font3", "font4", "font5", "font6"]:
            font_choice = font_input
        elif font_input:
            print("خطأ: الخط غير معروف، سيتم استخدام font1")

        word = input("اكتب كلمتك: ")

## فحص المدخلات وطباعة النتيجة
if (len(word) < 1 or
    word == " "):
        print("أدخل كلمة أو حرف.")
elif is_arabic(word):
    printable = letters_locations(word)
    printletters(printable, font_choice, color_choice, no_dots)
else:
    print("النص الذي أدخلته يحتوي على حروف غير عربية.")
