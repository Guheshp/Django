import random

available_numbers = [x for x in range(5)]  # 0 to 5
size = 7

def generate_invoice_number():
    new_number_list = [str(random.choice(available_numbers)) for _ in range(size)]
    new_number_str = "".join(new_number_list) 
    return new_number_str
