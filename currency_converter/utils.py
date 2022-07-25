
import csv
import json
from locale import currency
import sys
import requests
import os
import logging
from tkinter import *
from paths import *
from datetime import datetime

if __name__ == "__main__":
    sys.exit("Not runnable module")

# functions
def get_current_rates(): # get all rates

    rates = []
    current_date = datetime.today().strftime("%y-%m-%d")
    # check rates file to update
    # check folder 
    online_request = True
    for f_name in os.listdir(DATA_FOLDER):
        split_name = f_name.split("_")
        if split_name[0] != "rates": continue
        if split_name[1].replace(".json", "") == current_date: 
            online_request = False
            break

    # get file if up to date
    if online_request:
        API = "At27WyK4M2IoFbO9PCK5VT3qVPOA8Ytc"
        URL = F"http://api.exchangeratesapi.io/v1/latest?access_key={API}"
        response_string = requests.get(URL, headers = {"UserAgent":"XY"})
        
        #convert to json
        rates = json.loads(response_string.text)

        # save file
        with open (DATA_FOLDER.joinpath(f"rates_{current_date}.json"), "w", encoding="utf-8") as f:
            json.dump(rates, f)
            pass

        pass
    
    with open (DATA_FOLDER.joinpath(f"rates_{current_date}.json"), encoding="utf-8") as f:
        rates = json.load(f)

    return rates

def calculate_result(from_currency, to_currency, amount) -> dict: # get data by user input

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"

    payload = {}
    headers= {
    "apikey": "At27WyK4M2IoFbO9PCK5VT3qVPOA8Ytc"
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    result = json.loads(response.text)

    return result

def display_result_and_logging(result): # create text object 
    
    string_to_print = f"{result['query']['amount']} {result['query']['from']} = {round(result['result'], 2)} {result['query']['to']}"

    result_text = Label(text = string_to_print, font = ("Segoe UI Black bold", "30"))
    result_text.pack()

    logging.basicConfig(
    filename=LOG_FILE_NAME, 
    encoding="utf-8", 
    level=logging.INFO,
    format="%(asctime)s; %(message)s")

    logging.info(string_to_print)


    pass


# check if input was by currency code, by country, by another data and turn into one format (currency code)
def check_formate_user_input(input): 
    
    with open(COUNTRIES_DATA_FILE , encoding="utf-8") as f:
        countries = json.load(f) # convert to list of dictionary 
        pass

    for country in countries:
        for next_element in country.values():
            if next_element == input: 
                currency = country['currency_code']
                break
            
            else: continue

        pass

    pass

    return currency

#print (calculate_result("USD", "EUR", "90")) # TEST PRINT 

def main():
    # window object
    window = Tk()
    window.title("Currency converter")
    window.geometry("1000x600")

    # headers objects:
    header_1 = Label(text = "\nCurrency converter\n", font = ("Impact bold", "40"))
    header_1.pack()

    header_2 = Label(text = "Input information below:\n")
    header_2.pack()

    # input objects:
    # first currency input
    from_header = Label (text = "From:")
    from_header.pack()

    first_as_stringvar = StringVar()
    first_input = Entry(textvariable= first_as_stringvar)
    first_input.focus()
    first_input.pack()


    # amount input
    amount_header = Label(text = "Amount:")
    amount_header.pack()

    amount_as_stringvar = StringVar()
    amount_input = Entry(textvariable= amount_as_stringvar)
    #amount_input.focus()
    amount_input.pack()


    # second currency input
    second_header = Label(text = "To:")
    second_header.pack()

    second_as_stringvar = StringVar()
    second_input = Entry(textvariable= second_as_stringvar)
    #second_input.focus()
    second_input.pack()

    # "Calculate" button func
    def calculate_and_print ():
        # save StringVar to variables
        first_currency = check_formate_user_input(first_as_stringvar.get())
        second_currency = check_formate_user_input(second_as_stringvar.get())
        amount = amount_as_stringvar.get() # -> str 
        
        result_dict = calculate_result(first_currency, second_currency, amount)
        #print (result_dict)  TEST
        
        display_result_and_logging(result_dict)
        pass

    #
    # print result with button object
    result_button = Button(text= "Calculate",width= 10, command = calculate_and_print)
    result_button.pack(pady=20)

    # "Show conversations history" button func
    def show_history():
        # create text from csv data file
        with open (LOG_FILE_NAME) as f:
            history_list = list(csv.reader(f, delimiter = ","))
            pass

        history = ""
        for event in history_list:
            history += f"{event[0]}:\t{event[1][5:]}\n\n" 

        # open new window
        new_window = Toplevel(window)
        new_window.geometry("600x400")
        new_window.title("History")

        # add skrollbar on window
        v = Scrollbar(new_window)
        v.pack(side = RIGHT, fill = Y)

        # create history text as object
        history_text = Label (new_window, text = history)
        history_text.pack(side = "left")
        history_text.place(x=1, y= 1)

        # accept delete function
        def accept_delete():
            new_window_accept = Toplevel(new_window)
            new_window_accept.geometry("400x250")

            # question text
            quetion = Label(new_window_accept, text = "Do you want to clear history?")
            quetion.pack()

            # accept delete button
            clear_history_button2 = Button(new_window_accept, text = "Clear data", width= 10, command= delete_history)
            clear_history_button2.pack(pady=20)

            # cancel delete button
            cancel_button = Button (new_window_accept, text= "Cancel", width= 10, command= new_window_accept.destroy)
            cancel_button.pack(pady= 20)

        # open delete menu button
        clear_history_button1 = Button(new_window, text="Clear data", width= 10, command= accept_delete)
        clear_history_button1.pack(pady= 20)
        clear_history_button1.place(x=400, y = 50)
        
        # close history button
        close_history_button = Button(new_window, text = "Close history", width=10, command= new_window.destroy)
        close_history_button.pack(pady= 20)
        close_history_button.place(x=400, y=100)
        
        pass

    # function to clear log file and restart script to close all windows 
    def delete_history():
        f = open(LOG_FILE_NAME, "w")
        f.truncate()
        f.close()
        
        # restart main script
        os.execv(sys.executable, ['python'] + sys.argv)

        pass

    # create show history button
    history_button = Button(text = "Show conversations history", width= 20, command= show_history)
    history_button.pack(pady= 20)
    history_button.place(x= 10, y= 10)

    date_text = f"Currency rate from {datetime.today()}"

    # date text
    date = Label (text = date_text[:-7])
    date.place(relx = 0.0,
                rely = 1.0,
                anchor ='sw')

    mainloop()
