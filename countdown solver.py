#https://github.com/lse30/Countdown_solver/blob/master/countdown%20solver.py

import time
import random
import re
from itertools import permutations
from itertools import combinations_with_replacement
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()


pdf_cozumlu = FPDF()
pdf_cozumlu.add_page()

def solver(numbers, target):
    start_time = time.time()
    num_orders = []
    used_nums = []

    num_orders = list(permutations(number_list))


    operators = ['a','s','m','d']
    op_sequence = []
    for operator_1 in operators:
        for operator_2 in operators:
            for operator_3 in operators:
                for operator_4 in operators:
                    for operator_5 in operators:
                        op_list = [operator_1, operator_2, operator_3, operator_4, operator_5]
                        op_sequence.append(op_list)

    op1_sequence = list(combinations_with_replacement(operators, 5))

    for num_order in num_orders:
        for sequence in op1_sequence:
            sequence = list(sequence)
            i = 0
            while i <= 5:

                if i == 0:
                    current = num_order[0]
                else:
                    if sequence[i-1] == 'a':
                        current += num_order[i]
                    elif sequence[i-1] == 's':
                        current -= num_order[i]
                    elif sequence[i-1] == 'm':
                        current *= num_order[i]
                    else:
                        current /= num_order[i]

                if current == target:
                    start = str(num_order[0])
                    basla = num_order[0]

                    j = 0
                    while j < i:
                        tmp = basla
                        if sequence[j] == 'a':
                            use = '+'
                            basla = basla + num_order[j+1]
                        elif sequence[j] == 's':
                            use = '-'
                            basla = basla - num_order[j+1]
                        elif sequence[j] == 'm':
                            use = '*'
                            basla = basla * num_order[j+1]
                        else:
                            use = '/'
                            basla = basla / num_order[j+1]
                        if j==0:
                            string = use + str(num_order[j+1]) + "=" + str(basla) + ",     "
                        else:
                            string = str(tmp) + use + str(num_order[j+1]) + "=" + str(basla) + ",     "
                        start += string
                        j += 1
                    time_elapsed = time.time()
                    print('time taken: ', (time_elapsed-start_time))

                    return start


                i += 1

# rastgele sayı ürettiğimiz bölüm
def number_generator():
    num_list = []
    target = random.randint(200, 999)
    num_list.append(random.randint(1, 10))
    num_list.append(random.randint(1, 10))
    num_list.append(random.randint(1, 10))
    num_list.append(random.randint(1, 10))
    num_list.append(random.randint(1, 4) * 25)
    num_list.append(random.randint(1, 4) * 25)
    return(target, num_list)

#ürettiğimiz sayıları pdf dökümanını yazıyoruz
def write_pdf(target_num,nums,answers):
    for i in range(len(target_num)):

        #hedef sayıyı yaz
        pdf.set_font('Times', 'B', 20)
        pdf.cell(200, 15, txt=str(target_num[i]), ln=1, align="C")

        pdf_cozumlu.set_font('Times', 'B', 20)
        pdf_cozumlu.cell(200, 15, txt=str(target_num[i]), ln=1, align="C")
        #kullanılacak sayilari yaz
        pdf.set_font('Times', 'B', 14)
        pdf_cozumlu.set_font('Times', 'B', 14)

        values = '                 '.join(str(v) for v in nums[i])
        pdf.cell(200,10,txt= values, ln=1, align='C')
        pdf_cozumlu.cell(200,10,txt= values, ln=1, align='C')
        #çözümü yazar
        cevap = 0

        pdf_cozumlu.cell(200,75, txt="",ln = 1, align='C')

        pdf.cell(200, 105, txt="", ln=1, align='C')
        pdf_cozumlu.cell(200, 10, txt=str(answers[i]), ln=1, align='C')

        pdf_cozumlu.cell(200,20, txt="",ln = 1, align='C')



# rastgele sayı üretimi biter

#sayıları fonksiyonlara gönderip çözüm için beklediğimiz bölüm

countdown_number = []
countdown_target = []
countdown_answer = []
hedef, number_list = number_generator()
answer = solver(number_list, hedef)

for i in range(10): #range(10)--> generate 10 question

    while answer == None:
        number_list = []
        hedef, number_list = number_generator()
        answer = solver(number_list, hedef)

    print(answer)
    countdown_target.append(hedef)
    countdown_number.append(number_list)
    countdown_answer.append(answer)
    hedef, number_list = number_generator()
    answer = solver(number_list, hedef)

write_pdf(countdown_target, countdown_number, countdown_answer)
pdf.output('countdown.pdf')
pdf_cozumlu.output('countdown_solutions.pdf')
