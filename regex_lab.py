reg = "ab+cd"
reg = "ab[cd]*|bca"
reg = "ab(c|(d|b))v|bas+" # пока вложенные скобки игнорируем! и такое не трогаем, давайте уже после майских, коллеги


### функция разделяет регулярку на элементы, собираем список списков
# если буква, кладём в список
# если оператор +*, дополняем этим оператором (что делать со звёздочкой? кажется, заменяем на плюс)
# если оператор [ или ( -- хранить уровень глубины (вложенности скобок) c 0


[['a'], ['b'], [['c'], ['(d|b)']], ['v']] | [['b'], ['a'], ['s+']]
# ['a', 'b+', 'c', 'd']

[['a'], ['b'], ['[cd]*']] | ['b', 'c', 'a']


### функция, составляющая правила на основе этих элементов (всё запихиваем в список словарей dicts)

reg = "ab+cd" # регулярка, по которой собираем список правил

S = {{}: ''}
A = {S: 'a'}
B = {
        A: 'b',
        B: 'b'
    }
C = {B: 'c'}
D = {C: 'd'}

dicts = [A, B, C, D]

check = "abcd" # последовательность, которую разбираем

N = S # переменная для вершины
symb = '' # записать сюда первый символ входящей последовательности

for dic in dicts:
    if N in dic.keys() and dicts[N] == symb:
        ...
        N = dic.keys() # актуальная переменная

### функция, которая проверяет подходит ли другая строка под эти правила