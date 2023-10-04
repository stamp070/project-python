from datetime import datetime
from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import csv
import subprocess

root = Tk()
root.title("โปรแกรมรายรับ-รายจ่าย")
root.geometry("1200x1000")
root.resizable(False,False)

#function (menu)
def About():
    tkinter.messagebox.showinfo("โปรแกรมรายรับ-รายจ่าย","สร้างโดย นาย วรธน มีมูล 6604062630498 กับ  นาย ภัทรกร ยุทธเทพา 6604062630412")
def Exit():
    confirm = tkinter.messagebox.askquestion("ยืนยันการปิดโปรแกรม","ต้องการปิดโปรแกรมมั้ย ?")
    if confirm == "yes":
        root.destroy()

myMenu = Menu()
root.config(menu=myMenu)

#Sub Menu
menuitem = Menu()
menuitem.add_command(label="About",command=About)
menuitem.add_command(label="Exit",command=Exit)

#main Menu
myMenu.add_cascade(label="File",menu=menuitem)

#tabs
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Helvetica", 16))
style.configure("TNotebook.Tab", padding=[20, 10])

notebook = ttk.Notebook(root)


tab1 = Frame(notebook,width=1200,height=1000)
tab2 = Frame(notebook,width=1200,height=1000)
tab3 = Frame(notebook,width=1200,height=1000)

notebook.add(tab1 ,text="รายรับ")
notebook.add(tab2 ,text="รายจ่าย")
notebook.add(tab3 ,text="สรุป")
notebook.grid(row=0,column=0,sticky=NW)

#variable
data_income_dict = {}
data_expenses_dict = {}

income_date = StringVar()

income_str = StringVar()
income_num = StringVar()
expenses_str = StringVar()
expenses_num = StringVar()
comment_var = StringVar()

output_entry1 = IntVar()
output_entry2 = IntVar()
output_entry3 = IntVar()

#function
def save_data(date_detail, data_dict, show_data, entry_detail, entry_amount, label_warn):
    date = date_detail.get_date()
    date_str = date.strftime('%d/%m/%Y') #เอามาเพื่อเปลี่ยนเป็น วว/ดด/ปป
    detail = entry_detail.get()
    num = entry_amount.get()
    comment = comment_var.get()
    time = datetime.now().strftime('%H:%M:%S')

    try:
        num = int(num)

        label_warn.config(text='')
        label_warn.config(fg='white')
    except ValueError:
        label_warn.config(text='จำนวนที่คุณกรอกไม่ใช่ตัวเลข กรุณาลองใหม่')
        label_warn.config(fg='red')

        selected_item = show_data.selection()
        if selected_item:
            show_data.delete(selected_item)
        return

    key = (f"{date_str} {time}")
    data_dict[key] = {'Date': date_str, 'Detail': detail, 'Amount': num, 'Comment': comment}
    show_data.insert('', 'end', values=(date_str, detail, num, comment))

    print('income: ', data_income_dict)
    print('expenses: ', data_expenses_dict)

    return data_dict

def load_data(data_income_dict, data_expenses_dict):

    total_income_amount = sum(int(entry.get('Amount', 0)) for entry in data_income_dict.values())
    total_expenses_amount = sum(int(entry.get('Amount', 0)) for entry in data_expenses_dict.values())

    output_entry1.set(total_income_amount)
    output_entry2.set(total_expenses_amount)
    output_entry3.set(abs(total_income_amount-total_expenses_amount))
    print(total_income_amount)
    print(total_expenses_amount)

    if total_income_amount > total_expenses_amount:
        label_sum4.config(text='เยี่ยมเลยคุณสามารถเก็บเงินได้ {} บาท'.format(total_income_amount-total_expenses_amount))
        label_sum4.config(fg='green')

    elif total_income_amount == total_expenses_amount : 
        label_sum4.config(text='คุณได้ใช้เงินเท่ากับที่ได้รับมา {} บาท'.format(total_income_amount-total_expenses_amount))
        label_sum4.config(fg='orange')

    else:
        label_sum4.config(text='คุณใช้เงินมากว่ารายรับ {} บาท'.format(total_expenses_amount-total_income_amount))
        label_sum4.config(fg='red')


def export_to_csv():
    try:
        with open('income_expenses.csv', 'w', newline='\n', encoding='utf-8') as csvfile:
            fieldnames = ['Type', 'Date', 'Detail', 'Amount', 'Comment']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for date, entry in data_income_dict.items():
                entry['Type'] = 'Income'
                writer.writerow(entry)

            for date, entry in data_expenses_dict.items():
                entry['Type'] = 'Expenses'
                writer.writerow(entry)

        # แยก total income กับ total expenses
        total_income = sum(entry['Amount'] for entry in data_income_dict.values())
        total_expenses = sum(entry['Amount'] for entry in data_expenses_dict.values())

        # แยกไฟล์ total ไว้
        with open('totals.csv', 'w', newline='\n', encoding='utf-8') as totalsfile:
            totals_writer = csv.DictWriter(totalsfile, fieldnames=['Type', 'Total'])
            totals_writer.writeheader()
            totals_writer.writerow({'Type': 'Income', 'Total': total_income})
            totals_writer.writerow({'Type': 'Expenses', 'Total': total_expenses})

        label_sum5.config(text='Data exported to income_expenses.csv and totals.csv', fg='green')

        subprocess.Popen(['start', 'income_expenses.csv'], shell=True)

    except Exception as e:
        label_sum5.config(text='Error exporting data: {}'.format(str(e)), fg='red')



def load_data_from_csv():
    try:
        # ลบ Data ในviewtree
        show_data_income.delete(*show_data_income.get_children())
        show_data_expenses.delete(*show_data_expenses.get_children())

        with open('income_expenses.csv', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date_str = row['Date']
                if row['Type'] == 'Income':
                    data_income_dict[date_str] = {
                        'Date': date_str,
                        'Detail': row['Detail'],
                        'Amount': int(row['Amount']),
                        'Comment': row['Comment']
                    }
                    show_data_income.insert('', 'end', values=(date_str, row['Detail'], int(row['Amount']), row['Comment']))
                elif row['Type'] == 'Expenses':
                    data_expenses_dict[date_str] = {
                        'Date': date_str,
                        'Detail': row['Detail'],
                        'Amount': int(row['Amount']),
                        'Comment': row['Comment']
                    }
                    show_data_expenses.insert('', 'end', values=(date_str, row['Detail'], int(row['Amount']), row['Comment']))
        
        # Load totals from totals.csv
        with open('totals.csv', 'r', newline='', encoding='utf-8') as totalsfile:
            totals_reader = csv.DictReader(totalsfile)
            for row in totals_reader:
                if row['Type'] == 'Income':
                    output_entry1.set(int(row['Total']))
                    total_income = int(row['Total'])
                elif row['Type'] == 'Expenses':
                    output_entry2.set(int(row['Total']))
                    total_expenses = int(row['Total'])
        
        if total_income > total_expenses:
            label_sum4.config(text='เยี่ยมเลยคุณสามารถเก็บเงินได้ {} บาท'.format(total_income-total_expenses))
            label_sum4.config(fg='green')

        elif total_income == total_expenses : 
            label_sum4.config(text='คุณได้ใช้เงินเท่ากับที่ได้รับมา {} บาท'.format(total_income-total_expenses))
            label_sum4.config(fg='orange')

        else:
            label_sum4.config(text='คุณใช้เงินมากว่ารายรับ {} บาท'.format(total_expenses-total_income))
            label_sum4.config(fg='red')

        # คำนวนสรุปจาก total.csv
        output_entry3.set(abs(int(output_entry1.get()) - int(output_entry2.get())))

        label_sum5.config(text='Data loaded from income_expenses.csv and totals.csv', fg='green')

    except Exception as e:
        label_sum5.config(text='Error loading data: {}'.format(str(e)), fg='red')



#page 1
Label_date_income = Label(tab1,text="กรุณาใส่วันที่ (วัน/เดือน/ปี)",font=('arial',15,'bold')).grid(row=0,column=0,padx=(50,0))
cal = DateEntry(tab1, font=('arial', 15, 'bold'), date_pattern='dd/MM/yyyy', textvariable=income_date)
cal.grid(row=1, column=0)

 

Label_detail_income = Label(tab1,text="กรุณากรอกรายการรายรับ",font=('arial',15,'bold')).grid(row=0,column=1,pady=(50))
ety_detail_income = Entry(tab1,width='30',font=('arial',15,'bold'), textvariable=income_str, justify='center').grid(row=1 , column= 1,)

Label_amount_income = Label(tab1,text="กรุณากรอกจำนวน (บาท)",font=('arial',15,'bold')).grid(row=3,column=1,pady=(40,20))
ety_amount_income = Entry(tab1,width='30',font=('arial',15,'bold'), textvariable=income_num, justify='center').grid(row=4 , column= 1,)

option = ttk.Combobox(tab1,state="readonly",values=["เงินสด", "เงินโอน"],width='18',font=('arial',15,'bold'), textvariable=comment_var).grid(row=5,column=1,pady=(30,0),)
comment_var.set(value='เงินสด')

btn_save = Button(tab1, text="บันทึก", font=('arial', 15, 'bold'),
                  command=lambda: [save_data(cal, data_income_dict, show_data_income, income_str, income_num, label_warn1),
                                   load_data(data_income_dict, data_expenses_dict)]).grid(row=6, column=1, pady=(20, 0))
label_warn1 = Label(tab1, text='',font=('arial',25,'bold'))
label_warn1.grid(columnspan=2, row=8, pady=40)

show_data_income = ttk.Treeview(tab1, columns=('Date','Detail','Amount','Comment'),show='headings')

show_data_income.heading('Date', text='วันที่')
show_data_income.heading('Detail', text='รายการ')
show_data_income.heading('Amount', text='จำนวนเงิน')
show_data_income.heading('Comment', text='หมายเหตุ')

show_data_income.column('Date', width=250, anchor='center')
show_data_income.column('Detail', width=250, anchor='center')
show_data_income.column('Amount', width=250, anchor='center')
show_data_income.column('Comment', width=250, anchor='center')

vsb = ttk.Scrollbar(tab1, orient="vertical", command=show_data_income.yview)
vsb.grid(row=7, column=2, pady=30)

show_data_income.configure(yscrollcommand=vsb.set)
show_data_income.grid(row=7,columnspan=2, pady=30,padx=(100,0))

#page 2 

Label_date_income = Label(tab2,text="กรุณาใส่วันที่ (วัน/เดือน/ปี)",font=('arial',15,'bold')).grid(row=0,column=0,padx=(50,0))
cal = DateEntry(tab2, font=('arial', 15, 'bold'), date_pattern='dd/MM/yyyy', textvariable=income_date)
cal.grid(row=1, column=0)

Label_detail_income = Label(tab2,text="กรุณากรอกรายการรายจ่าย",font=('arial',15,'bold')).grid(row=0,column=1,pady=(50))
ety_detail_income = Entry(tab2,width='30',font=('arial',15,'bold'), textvariable=expenses_str, justify='center').grid(row=1 , column= 1,)

Label_amount_income = Label(tab2,text="กรุณากรอกจำนวน (บาท)",font=('arial',15,'bold')).grid(row=3,column=1,pady=(40,20))
ety_amount_income = Entry(tab2,width='30',font=('arial',15,'bold'), textvariable=expenses_num, justify='center').grid(row=4 , column= 1,)

option = ttk.Combobox(tab2,state="readonly",values=["เงินสด", "เงินโอน"],width='18',font=('arial',15,'bold'), textvariable=comment_var).grid(row=5,column=1,pady=(30,0),)
comment_var.set(value='เงินสด')

btn_save = Button(tab2,text="บันทึก",font=('arial',15,'bold'),
                  command=lambda: [save_data(cal, data_expenses_dict, show_data_expenses, expenses_str, expenses_num, label_warn2), 
                                                                               load_data(data_income_dict,data_expenses_dict)]).grid(row=6,column=1,pady=(20,0),)

label_warn2 = Label(tab2, text='',font=('arial',25,'bold'))
label_warn2.grid(columnspan=2, row=8, pady=40)

show_data_expenses = ttk.Treeview(tab2, columns=('Date','Detail','Amount','Comment'),show='headings')

show_data_expenses.heading('Date', text='วันที่')
show_data_expenses.heading('Detail', text='รายการ')
show_data_expenses.heading('Amount', text='จำนวนเงิน')
show_data_expenses.heading('Comment', text='หมายเหตุ')

show_data_expenses.column('Date', width=250, anchor='center')
show_data_expenses.column('Detail', width=250, anchor='center')
show_data_expenses.column('Amount', width=250, anchor='center')
show_data_expenses.column('Comment', width=250, anchor='center')

vsb = ttk.Scrollbar(tab2, orient="vertical", command=show_data_expenses.yview)
vsb.grid(row=7, column=2, pady=30)

show_data_expenses.configure(yscrollcommand=vsb.set)
show_data_expenses.grid(row=7,columnspan=2, pady=30,padx=(100,0))

#page 3
Label_total_income = Label(tab3,text="คุณได้รับเงินมาทั้งหมด",font=('arial',15,'bold')).grid(row=0,column=0,padx=(500),pady=60)
ety_total_income = Entry(tab3,width='50',font=('arial',15,'bold'), textvariable=output_entry1, justify='center',state='readonly').grid(row=1 , column= 0)
Label_total_expanses = Label(tab3,text="คุณได้ใช้เงินไปทั้งหมด",font=('arial',15,'bold')).grid(row=2,column=0,padx=(500),pady=60)
ety_total_income = Entry(tab3,width='50',font=('arial',15,'bold'), textvariable=output_entry2, justify='center',state='readonly').grid(row=3 , column= 0)
total_all = Label(tab3,text="สรุปการใช้เงิน",font=('arial',15,'bold')).grid(row=4,column=0,padx=(500),pady=60)
total_all = Entry(tab3,width='50',font=('arial',15,'bold'), textvariable=output_entry3, justify='center',state='readonly').grid(row=5 , column= 0)

export_btn = Button(tab3,text="Export to CSV",width=20,font=('arial',15,'bold'),command=export_to_csv).grid(row=6,column=0,pady=15)
Import_btn = Button(tab3,text="Import to CSV",width=20,font=('arial',15,'bold'),command=load_data_from_csv).grid(row=7,column=0,pady=15)

label_sum4 = Label(tab3, text='',font=('arial',25,'bold'))
label_sum4.grid(column=0, row=8, pady=40)

label_sum5 = Label(tab3, text='',font=('arial',15,'bold'))
label_sum5.grid(column=0, row=9, pady=40)

root.mainloop()