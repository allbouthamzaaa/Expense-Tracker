import time 
from datetime import datetime
import csv

class PreferenceNotExists(Exception):
    pass
class FileEmpty(Exception):
    pass

class NegativeValueError(Exception):
    pass

class LimitedCharacterRange(Exception):
    pass

class DateNotFound(Exception):
    pass


print("----WELCOME TO THE GULUB EXPANSE TRACKER----")
print()
print(f"PRESS ANY KEY TO SEE THE MENU:) ",end="")
input()

def get_choice():
     while True:
        try:
            choice = input("Enter Your preference: ").strip()
            if choice not in ['1','2','3','4','5']:
                raise PreferenceNotExists("Invalid preference , should be in 1 to 5")
                
        except PreferenceNotExists as err:
            print(f'Error: {err}')
        else:
            return choice
            
def get_amount():
    while True:
        try: 
            amount = int(input("Enter the spent amount: "))
            if amount < 0:
                raise NegativeValueError("Invalid input, Amount should be in positive numbers")
            elif amount == 0:
                print("Amount must be greater than zero")
                continue
        except ValueError:
            print("Invalid input, should be an integer")
        except NegativeValueError as err:
            print(f"ERROR: {err}")        
        else:
            return amount
            
def get_category(amount):
    
    while True:
        try:
            category = input(f"In which Category you spent {amount}rs: ").strip()
            if not category.isalpha():
                raise ValueError("Invalid input , Enter the category name in proper letter")
        except ValueError as err:
            print(f"ERROR: {err}")     
        else:
            return category
                
def get_note():
    
    while True:
        try:
            note = input("Enter your description on this expense: ").strip().replace(",","-")
            if len(note)>100:
                raise LimitedCharacterRange("Maximum 100 character Should be in note")
            elif len(note)<3:
                raise LimitedCharacterRange("Minimum 3 characters must required in note")
            else:
                return note
            
        except LimitedCharacterRange as err:
            print(f"ERROR: {err}")                 


def add_expense():
    amount = get_amount()
    expense_data = {
        'AMOUNT' : amount,
        'CATEGORY': get_category(amount),
        'DESCRIPTION': get_note(),
    }
    current = datetime.now()
    expense_data['TIME'] = current.strftime('%H:%M:%S')
    expense_data['DATE'] = current.strftime("%d-%m-%Y")
    try:
        with open('_expense_data.csv','a') as f:
            f.write(",".join(str(data) for data in expense_data.values()))
            f.write('\n')      
            print("ADDED")
    except PermissionError:
        print('ERROR: This file is open somewhere most probabily')
        
    return True    


def view_today_data():
    print()
    try:
        found = False
        date = datetime.now()
        with open('_expense_data.csv','r') as f:
            expense_data = csv.DictReader(f)
            total  = 0 
            today_date = date.strftime("%d-%m-%Y")
            for data in expense_data:
                if data['DATE'] == today_date:
                    if not found:
                        print(f"{'AMOUNT':^15}|{'CATEGORY':^15}|{'SPENT ON':^20}")
                        found = True
                    total += int(data['AMOUNT'])
                    print(f"{data['AMOUNT']:^15}|{data['CATEGORY']:^15}|{data['DESCRIPTION']:^20}")
                
        if found:        
            print()
            print("=================================================")
            print(f"||   TOTAL EXPENSE on {today_date} : {total}rs    ||")
            print("=================================================")
        else:
            print(f"     NO EXPENSES ON {today_date}            ")                
                        
                    
    except FileEmpty as err:
        print(f"ERROR: {err}")     
    except FileNotFoundError:
        print("The file does not exists in your folder")      
                
    return True   

def get_date():
    while True:
        try:
            date = input("Enter the date which you want to search(01-30/31): ").strip()
            if int(date)>31:
                print("Invalid date input , should be between 1 to 30/31")
                continue
            elif int(date)<=0:
                 raise NegativeValueError("Invalid input , date should be positive")
        except NegativeValueError as err:
            print(f"ERROR: {err}")    
        except ValueError:
                print("Invalid input , Try again")        
        else:
            return date if len(date)>1 else '0' + date
     
def get_month():
    while True:
        try:
            month = input("Enter the month which you want to search(01-12): ").strip()
            if int(month)>12:
                print("Invalid date input , should be between 1 to 12")
                continue
            elif int(month)<0:
                 raise NegativeValueError("Invalid input , date should be positive")
        except NegativeValueError as err:
            print(f"ERROR: {err}")    
        except ValueError:
                print("Invalid input , Try again")        
        else:
            return month if len(month)>1 else '0' + month

def get_year():
    while True:
        curr_year = datetime.now().strftime('%Y')
        try:
            year = input("Enter the year which you want to search: ").strip()
            if int(year) > int(curr_year) or int(year)<2000:
                print(f"Invalid input , enter proper year")
                continue
            elif int(year)<0:
                raise NegativeValueError("Invalid input , year should positive and 21st century")
        except NegativeValueError as err:
            print(f'ERROR: {err}')  
        except ValueError:
            print("Invalid input , Try again")    
        else:
            return year            
        
    
        
def view_by_date():
    search_date = get_date()
    search_month = get_month()
    search_year = get_year()
    desired_moment = search_date + "-" + search_month + "-" + search_year
    
    print()
    text = 'finding.....!'
    for ch in text:
        time.sleep(0.15)
        print(ch, end="")
    print()   
    try:
        with open('_expense_data.csv','r') as f:
            expense_data = csv.DictReader(f)
            found = False
            for data in expense_data:   
                if data['DATE'] == desired_moment:
                    if not found:
                        print("FOUND")
                        print(f"{'AMOUNT':^15}|{'CATEGORY':^15}|{'SPENT ON':^20}|{'TIME':^15}")
                        found = True   
                    print(f"{data['AMOUNT']:^15}|{data['CATEGORY']:^15}|{data['DESCRIPTION']:^20}|{data['TIME']:^15}")
                    
            if not found:
                print("THE DESIRED DATE NOT FOUND IN THE DATA BASE")    
                another = False
                while True:
                        
                    check = input("WOULD YOU LIKE TO CHECK ANOHER DATE(Y/N)? ").strip().upper()
                    if check not in ['Y','N']:
                        print("INVALID INPUT , SHOULD IN BE YES OR NO")
                    elif check == 'Y':
                        another = True
                        break
                    else: break
                if another:
                    view_by_date()    
    except FileNotFoundError:
        print("THE REQUIRED FILE DOES NOT EXISTS IN DATABASE")
                             
    return True

def each_date_total():
    date = get_date()
    month = get_month()
    year = get_year()
    desired_time = date + '-' + month + '-' + year
    
    print()
    try:
        with open('_expense_data.csv' , 'r') as f:
            expense_data = csv.DictReader(f)
            found = False
            total = 0
            for data in expense_data:
                if data['DATE'] == desired_time:
                    total += int(data['AMOUNT'])
                    found = True
            if found:
                print("==========================================")
                print(f"||  TOTAL EXPENSE ON {desired_time} : {total}   ||")   
                print("==========================================")       
            else:
                print("THE REQUIRED DATA DOES NOT FOUND IN OUR DATA BASE")    
                another = False
                while True:
                        
                    check = input("WOULD YOU LIKE TO CHECK ANOHER DATE(Y/N)? ").strip().upper()
                    if check not in ['Y','N']:
                        print("INVALID INPUT , SHOULD IN BE YES OR NO")
                    elif check == 'Y':
                        another = True
                        break
                    else: break
                if another:
                    each_date_total()
                    
    except FileNotFoundError:
        print('THE REQUIRED FILE DOES NOT FOUND IN OUR DATABASE')                    
    
    return True                        
    
    
    
    
        
def ask_for_exit():
    while True:
        ask = input("DO YOU WANT TO EXIT(Y/N): ").upper()
        if ask not in ('Y','N'):
            print("Invalid input , should be Y or N ")
        elif ask == 'Y':
            return True
        else:
            return False


def want_to_continue():
    while True:
        print()
        _continue_ = input("Do you want to do something else(Y/N): ").upper()
        if _continue_ not in('Y','N'):
            print("Invalid input,Should be Y or N")
            continue
        return True if _continue_ == 'Y' else False        
    

def menu():
    print()
    options =['1. ADD EXPENSE' ,
            '2. VIEW TODAY' , 
            '3. VIEW BY DATE' , 
            '4. SHOW TOTALS (/-DATE WISE)', 
            '5. SAVE & EXIT']
                
    for option in options:
        time.sleep(0.1)
        print(option)
    
    choice = get_choice()   
    
    match choice:
        case '1':
            return add_expense()
        case '2':
            return view_today_data()
        case '3':
            return view_by_date()
        case '4':
            return each_date_total()
        case '5':
            return False
while True:             
    _start_ = menu()
    if _start_:
        _continue_ = want_to_continue()
        if _continue_:
            continue
        else:
            break
    else:
        want_exit = ask_for_exit()
        if want_exit:
            break
        else:
            time.sleep(0.3)
            continue 