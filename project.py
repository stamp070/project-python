from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

mywin = Tk()
mywin.title('Income and expenses')
mywin.geometry('1200x1000')
mywin.resizable(False, False)

page1 = Frame(mywin)
page2 = Frame(mywin)
page3 = Frame(mywin)

page1.grid(row=0, column=0, sticky=NSEW)
page2.grid(row=0, column=0, sticky=NSEW)
page3.grid(row=0, column=0, sticky=NSEW)

# Variable
data_income_dict = {}
data_expenses_dict = {}
income_str = StringVar()
income_num = StringVar()
expenses_str = StringVar()
expenses_num = StringVar()
comment_var = StringVar()

output_entry1 = IntVar()
output_entry2 = IntVar()
output_entry3 = IntVar()

# Function
def save_data(data_dict, show_data, entry_detail, entry_amount):
    date = cal.get_date()
    date = date.strftime('%d-%m-%Y')
    time = datetime.now().strftime('%H:%M:%S')
    detail = entry_detail.get()
    num = entry_amount.get()
    comment = comment_var.get()

    key = (f"{date} {time}")
    data_dict[key] = {'Date': date, 'Time': time, 'Detail': detail, 'Amount': num, 'Comment': comment}
    
    show_data.insert('', 'end', values=(date, time, detail, num, comment))
    print('income: ',data_income_dict)
    print('expenses: ',data_expenses_dict)
    return data_dict

def load_data(data_income_dict, data_expenses_dict):
    total_income_amount = sum(int(entry.get('Amount', 0)) for entry in data_income_dict.values())
    total_expenses_amount = sum(int(entry.get('Amount', 0)) for entry in data_expenses_dict.values())
    
    output_entry1.set(total_income_amount)
    output_entry2.set(total_expenses_amount)
    output_entry3.set(abs(total_income_amount-total_expenses_amount))
    print(total_income_amount)
    print(total_expenses_amount)

    if total_income_amount >= total_expenses_amount:
        label_sum4.config(text='เยี่ยมเลยคุณสามารถดก็บเงินได้ {} บาท'.format(total_income_amount-total_expenses_amount))
        label_sum4.config(fg='green')
    else:
        label_sum4.config(text='คุณใช้เงินมากว่ารายรับ {} บาท'.format(total_expenses_amount-total_income_amount))
        label_sum4.config(fg='red')

# PAGE 1
btn_income = Button(page1, text='รายรับ',command=lambda: page1.tkraise(), font=('arial',10), width=7, height=2)
btn_income.grid(column=0,row=0)

btn_expenses = Button(page1, text='รายจ่าย',command=lambda: page2.tkraise(), font=('arial',10), width=7, height=2)
btn_expenses.grid(column=1,row=0)

btn_sum = Button(page1, text='สรุป',command=lambda: page3.tkraise(), font=('arial',10), width=7, height=2)
btn_sum.grid(column=2,row=0)

label_date = Label(page1, text='Date:', font=('arial', 15))
label_date.grid(column=2,row=1,pady=(30,0))

cal = DateEntry(page1, font=('arial',13),date_pattern='MM/dd/yyyy')
cal.grid(column=3,row=1,pady=(30,0))

label_1 = Label(page1, text='กรุณากรอกรายการรายรับ',font=('arial',18,'bold'))
label_1.grid(column=4,row=3,pady=30)

input_1 = Entry(page1, width='50',font=('arial',16), textvariable=income_str)
input_1.grid(column=4,row=4)
input_1.focus()

label_2 = Label(page1, text='จำนวนเงิน (บาท)',font=('arial',18,'bold'))
label_2.grid(column=4,row=5,pady=30)

input_2 = Entry(page1, width='50',font=('arial',16), textvariable=income_num)
input_2.grid(column=4,row=6)

combo = ttk.Combobox(page1,state="readonly", values=['เงินสด','เงินโอน'], font=('arial',15), textvariable=comment_var)
combo.current(0)
combo.grid(column=4,row=7, pady=30)

btn_save = Button(page1, text='บันทึก', font=('arial', 12),command=lambda: [save_data(data_income_dict, show_data_income, income_str, income_num), load_data(data_income_dict,data_expenses_dict)], width=7, height=2)
btn_save.grid(column=4,row=8)

show_data_income = ttk.Treeview(page1, columns=('Date','Time','Detail','Amount','Comment'),show='headings')

show_data_income.heading('Date', text='วันที่')
show_data_income.heading('Time', text='เวลา')
show_data_income.heading('Detail', text='รายการ')
show_data_income.heading('Amount', text='จำนวนเงิน')
show_data_income.heading('Comment', text='หมายเหตุ')

show_data_income.column('Date', width=120, anchor='center')
show_data_income.column('Time', width=120, anchor='center')
show_data_income.column('Detail', width=120, anchor='center')
show_data_income.column('Amount', width=120, anchor='center')
show_data_income.column('Comment', width=120, anchor='center')

scroll = ttk.Scrollbar(page1, orient="vertical", command=show_data_income.yview)
scroll.grid(column=5, row=9, pady=30, sticky='ns')

show_data_income.configure(yscrollcommand=scroll.set)
show_data_income.grid(column=4, row=9, pady=30)

# PAGE 2
btn_income = Button(page2, text='รายรับ',command=lambda: page1.tkraise(), font=('arial',10), width=7, height=2)
btn_income.grid(column=0,row=0)

btn_expenses = Button(page2, text='รายจ่าย',command=lambda: page2.tkraise(), font=('arial',10), width=7, height=2)
btn_expenses.grid(column=1,row=0)

btn_sum = Button(page2, text='สรุป',command=lambda: [page3.tkraise(),load_data(data_income_dict,data_expenses_dict)], font=('arial',10), width=7, height=2)
btn_sum.grid(column=2,row=0)

label_date = Label(page2, text='Date:', font=('arial', 15))
label_date.grid(column=2,row=1,pady=(30,0))

cal = DateEntry(page2, font=('arial',13),date_pattern='MM/dd/yyyy')
cal.grid(column=3,row=1,pady=(30,0))

label_1 = Label(page2, text='กรุณากรอกรายการรายจ่าย',font=('arial',18,'bold'))
label_1.grid(column=4,row=3,pady=30)

input_1 = Entry(page2, width='50',font=('arial',16), textvariable=expenses_str)
input_1.grid(column=4,row=4)
input_1.focus()

label_2 = Label(page2, text='จำนวนเงิน (บาท)',font=('arial',18,'bold'))
label_2.grid(column=4,row=5,pady=30)

input_2 = Entry(page2, width='50',font=('arial',16), textvariable=expenses_num)
input_2.grid(column=4,row=6)

combo = ttk.Combobox(page2,state="readonly", values=['เงินสด','เงินโอน'], font=('arial',15), textvariable=comment_var)
combo.current(0)
combo.grid(column=4,row=7, pady=30)

btn_save = Button(page2, text='บันทึก', font=('arial', 12),command=lambda: [save_data(data_expenses_dict, show_data_expenses, expenses_str, expenses_num), load_data(data_income_dict,data_expenses_dict)], width=7, height=2)
btn_save.grid(column=4,row=8)

show_data_expenses = ttk.Treeview(page2, columns=('Date','Time','Detail','Amount','Comment'),show='headings')

show_data_expenses.heading('Date', text='วันที่')
show_data_expenses.heading('Time', text='เวลา')
show_data_expenses.heading('Detail', text='รายการ')
show_data_expenses.heading('Amount', text='จำนวนเงิน')
show_data_expenses.heading('Comment', text='หมายเหตุ')

show_data_expenses.column('Date', width=120, anchor='center')
show_data_expenses.column('Time', width=120, anchor='center')
show_data_expenses.column('Detail', width=120, anchor='center')
show_data_expenses.column('Amount', width=120, anchor='center')
show_data_expenses.column('Comment', width=120, anchor='center')

scroll = ttk.Scrollbar(page2, orient="vertical", command=show_data_expenses.yview)
scroll.grid(column=5, row=9, pady=30, sticky='ns')

show_data_expenses.configure(yscrollcommand=scroll.set)
show_data_expenses.grid(column=4, row=9, pady=30)

# PAGE 3
btn_income = Button(page3, text='รายรับ',command=lambda: page1.tkraise(), font=('arial',10), width=7, height=2)
btn_income.grid(column=0,row=0)

btn_expenses = Button(page3, text='รายจ่าย',command=lambda: page2.tkraise(), font=('arial',10), width=7, height=2)
btn_expenses.grid(column=1,row=0)

btn_sum = Button(page3, text='สรุป',command=lambda: [page3.tkraise(),load_data(data_income_dict,data_expenses_dict)], font=('arial',10), width=7, height=2)
btn_sum.grid(column=2,row=0)

label_date = Label(page3, text='Date:', font=('arial', 15))
label_date.grid(column=2,row=1,pady=(30,0))

cal = DateEntry(page3, font=('arial',13),date_pattern='MM/dd/yyyy')
cal.grid(column=3,row=1,pady=(30,0))

label_sum1 = Label(page3, text='คุณได้รับเงินทั้งหมด',font=('arial',18,'bold'))
label_sum1.grid(column=4,row=3,pady=30,)

ent_sum1 = Entry(page3, width='50', font=('arial',16), state='readonly', readonlybackground='white', cursor='arrow', textvariable=output_entry1, justify='center')
ent_sum1.grid(column=4,row=4)

label_sum2 = Label(page3, text='คุณไช้เงินไปทั้งหมด',font=('arial',18,'bold'))
label_sum2.grid(column=4,row=5,pady=30)

ent_sum2 = Entry(page3, width='50', font=('arial',16), state='readonly', readonlybackground='white', cursor='arrow', textvariable=output_entry2, justify='center')
ent_sum2.grid(column=4,row=6)

label_sum3 = Label(page3, text='สรุปยอดเงิน',font=('arial',18,'bold'))
label_sum3.grid(column=4,row=7,pady=30)

ent_sum3 = Entry(page3, width='50', font=('arial',16), state='readonly', readonlybackground='white', cursor='arrow', textvariable=output_entry3, justify='center')
ent_sum3.grid(column=4,row=8)

label_sum4 = Label(page3, text='',font=('arial',25,'bold'))
label_sum4.grid(column=4, row=9, pady=40)

page1.tkraise()
mywin.mainloop()