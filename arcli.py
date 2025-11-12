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
## تتأكد الدالة من المسافات كذلك
## إن كان الحرف وحيدًا ترجع الدالة ملحق _وحيد للحرف لتطبعه وحيدًا
## إن كان الحرف في بداية الكلمة تعطيه الدالة ملحق _مبتدأ
## إن كان الحرف في الوسط وقبله حرف منفصل تعطيه الدالة ملحق _مبتدأ
## إن كان الحرف في الوسط وقبله حرف متصل تعطيه الدالة ملحق _وسط
## إن كان الحرف في النهاية وقبله حرف منفصل تعطيه الدالة ملحق _وحيد
## إن كان الحرف في النهاية وقبله حرف متصل تعطيه الدالة ملحق _منتهى
## 
## تنبيه في حالة إضافة خطوط عليك بإضافة الملحقات لكل الحروف
## الحروف المنفصلة المبتدأ كالوحيد، والوسط كالمنتهى
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
## كل حرف له 9 أسطر، انتبه لذلك إن صممت خطك الخاص
def printletters(lettersarray, fontname):
    try:
        fontname = fontname + ".txt"
        with open(fontname, 'r', encoding='utf-8') as font:
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
    ## هنا نطبع الأحرف، نطبع أول سطر من كل حرف ومن ثم نضيف سطرًا جديدًا لنبدأ بالأسطر التالية
    ## تطبع الدالة الأحرف من اليسار لليمين لتعرضها على الطرفية بشكل صحيح
    for line in range(10):
        for letter in reversed(startlines):
            printnow = letter[line]
            print(printnow[:-1], end='')
        print()


## الحصول على المدخلات من المستخدم
font_choice = "font1"  # الخط الافتراضي

if len(sys.argv) > 1:
    # فحص إذا كان أول مدخل هو اسم خط
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


## البرنامج يحتاج الكثير من التعديل، وهو في طور التطوير
## أرحب بأي تعديلات وتحسينات على الأداء عن طريق github
