import random

# спам фильтр, тут будут функции фильтры, которые возвращают число от 0 до 1
# потом можно или нужно будет добваить веса фильтрам
# на входе будут письма в формате из парсера 
# https://eml-parser.readthedocs.io/en/latest/#example-usage

def runForOneMail(oneMail):
    pass

def main():
    filters = [filter1,filter2,filter3,filter4]
    sum = 0
    for func in filters:
        a = func()
        sum += a
        print(sum, a)
    
    spamRate = sum/len(filters)
    print(spamRate)

def filter1():
    return random.random()
    
def filter2():
    return random.random()

def filter3():
    return random.random()

def filter4():
    return random.random()
