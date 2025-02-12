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
## https://github.com/alwaqad/arcli

import os

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
    letters = {
        'ا' ,'أ' ,'آ' ,
        'آ' ,'ب' ,'ت' ,
        'ث' ,'ج' ,'ح' ,
        'خ' ,'د' ,'ذ' ,
        'ر' ,'ز' ,'س' ,
        'ش' ,'ص' ,'ض' ,
        'ط' ,'ظ' ,'ع' ,
        'غ' ,'ف' ,'ق' ,
        'ك' ,'ل' ,'م' ,
        'ن' ,'ه' ,'ة' ,'و' ,'ؤ' ,
        'ي' ,'ى' ,'ئ' ,'ء',' '}
    isarabic = False
    for letter in word:
        for arletter in letters:
            if letter == arletter:
                isarabic = True
                break
            else:
                isarabic = False
    return isarabic

## دالة تتأكد من موضع كل حرف في الكلمة وتسمي كل حرف في القائمة بالملحق المناسب له
## تتأكد الدالة من المسافات كذلك
## إن كان الحرف وحيدًا ترجع الدالة ملحق _وحيد للحرف لتطبعه وحيدًا
## إن كان الحرف في بداية الكلمة تعطيه الدالة ملحق _مبتدأ
## إن كان الحرف في الوسط وقبله حرف منفصل تعطيه الدالة ملحق _مبتدأ
## إن كان الحرف في الوسط وقبله حرف متصل تعطيه الدالة ملحق _وسط
## إن كان الحرف في النهاية وقبله حرف منفصل تعطيه الدالة ملحق _وحيد
## إن كان الحرف في النهاية وقبله حرف متصل تعطيه الدالة ملحق _منتهى
## 
##تنبيه في حالة إضافة خطوط عليك بإضافة الملحقات لكل الحروف
## الحروف المنفصلة المبتدأ كالوحيد، والوسط كالمنتهى
def letters_locations(word):
    numberedword = list(word)
    if (len(word)>1):
        for i in range(len(word)):
            if (word[i] == " "):
                numberedword[i]="مسافة"
            else:
                if (i == 0):
                    if (is_connectable(numberedword[i])):
                        numberedword[i]=numberedword[i]+"_مبتدأ"
                    else:
                        numberedword[i]=numberedword[i]+"_وحيد"
                elif (i == (len(word)-1) or word[i+1] == " "):
                    if (is_connectable(word[i-1])):
                        numberedword[i]=numberedword[i]+"_منتهى"
                    else:
                        numberedword[i]=numberedword[i]+"_وحيد"
                else:
                    if (is_connectable(numberedword[i])):
                        if (is_connectable(word[i-1])):
                            numberedword[i]=numberedword[i]+"_وسط"
                        else:
                            numberedword[i]=numberedword[i]+"_مبتدأ"
                    else:
                        if (is_connectable(word[i-1])):
                            numberedword[i]=numberedword[i]+"_وسط"
                        else:
                            numberedword[i]=numberedword[i]+"_وحيد"    
    else:
        numberedword[0]=numberedword[0]+"_وحيد"
    return numberedword
    

## دالة تمر على الأسطر في ملف الخط وتضيف الأحرف في  قائمة ثم تطبعها
## كل حرف له 9 أسطر، انتبه لذلك إن صممت خطك الخاص
def printletters(lettersarray, fontname):
    fontname = fontname + ".txt"
    font = open(fontname)
    fontlines = font.readlines()
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
            # comment: 
        print()

                
## نطلب مدخل من المستخدم
word = input("اكتب كلمتك: ")
if (len(word) < 1 or
    word == " "):
        print("أدخل كلمة أو حرف.")
elif is_arabic(word):
    printable = letters_locations(word)
    ## font1 هو اسم الخط المستخدم
    ## عندما أضيف ميزة كتابة الكلمة في نفس سطر تشغيل البرنامج سأضيف خاصية كتابة اسم الخط إن أراد المستخدم استخدام غيره
    printletters(printable, "font1")
else:
    print("النص الذي أدخلته يحتوي على حروف غير عربية.")


## البرنامج يحتاج الكثير من التعديل، وهو في طور التطوير
## أرحب بأي تعديلات وتحسينات على الأداء عن طريق github



