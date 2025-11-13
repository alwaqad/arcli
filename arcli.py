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

## https://github.com/alwaqad/arcli

import os
import sys

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
    

## دالة تمر على الأسطر في ملف الخط وتضيف الأحرف في  قائمة ثم تطبعها
def printletters(lettersarray, fontname):
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
                    startlines[x].append(fontlines[linenumber+i])
                x+=1
                break

    for line in range(10):
        for letter in reversed(startlines):
            printnow = letter[line]
            print(printnow[:-1], end='')
        print()


## الحصول على المدخلات من المستخدم
font_choice = "font1"

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

if (len(word) < 1 or
    word == " "):
        print("أدخل كلمة أو حرف.")
elif is_arabic(word):
    printable = letters_locations(word)
    printletters(printable, font_choice)
else:
    print("النص الذي أدخلته يحتوي على حروف غير عربية.")
