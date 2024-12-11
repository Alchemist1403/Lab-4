
def get_slots_and_new_points(stuffdict):
    '''Функция создаёт списки значений параметров вещей: 
    1) вместимость(количество слотов/мест в рюкзаке)
    2) очки выживания от предмета'''
    slots = [stuffdict[item][0] for item in stuffdict]
    new_points = [stuffdict[item][1] for item in stuffdict]     
    return slots, new_points


def get_memtable(stuffdict,bag):
    '''Функция создаёт таблицу для мемоизации'''
    slots, new_points = get_slots_and_new_points(stuffdict)
    number = len(new_points)

    table = [[0 for zero in range(bag+1)] for row in range(number+1)]

    for i in range(number+1):
        for a in range(bag+1):

            if i == 0 or a == 0:
                table[i][a] = 0

            elif slots[i-1] <= a:
                table[i][a] = max(new_points[i-1] + table[i-1][a-slots[i-1]], table[i-1][a])

            else:
                table[i][a] = table[i-1][a]
    return table, slots, new_points


def get_tools_list(stuffdict,bag):
    '''Функция создаёт список тех предметов, которые создают набор 
    с наибольшим количеством очков выживания'''
    table, slots, new_points = get_memtable(stuffdict,bag)

    n = len(new_points)
    res = table[n][bag]
    a = bag
    items_list = []

    for i in range(n, 0, -1):

        if res <= 0:
            break
        elif res == table[i-1][a]:
            continue

        else:

            items_list.append((slots[i-1], new_points[i-1]))
            res -= new_points[i-1]
            a -= slots[i-1]

    needed_items = []
    for i in range(len(items_list)):
        for item in toolsdict:
            if toolsdict[item][0] == items_list[i][0] and toolsdict[item][1] == items_list[i][1]:
                if item in needed_items:
                    continue
                else:
                    needed_items.append(item)
                    break

    return needed_items


toolsdict = {'r':(3,25),
             'p':(2,15),
             'a':(2,15),
             'm':(2,20),
             'k':(1,15),
             'x':(3,20),
             't':(1,25),
             'f':(1,15),
             'd':(1,10),
             's':(2,20),
             'c':(2,20)
            }

tools_slot1 = ['k','f','t','d']
tools_slot2 = ['p','a','m','s','c']
tools_slot3 = ['r','x']


taken_tools = get_tools_list(toolsdict,8)

surviving_points = 20  # 15 изначальных и 5 за ингалятор,т.к. в моём варианте это обязательный предмет.

for element in toolsdict:
    surviving_points -= toolsdict[element][1]

for element in taken_tools:
    surviving_points += 2*toolsdict[element][1]


matrix0 = [['i'],['1'],['1']]
matrix1 = [['1'],['1'],['1']]
matrix2 = [['1'],['1'],['1']]

while len(taken_tools) != 0:
    for tool in taken_tools:

        if tool in tools_slot3:
            if matrix1.count(['1']) == 3:
                matrix1[0] = tool
                matrix1[1] = tool
                matrix1[2] = tool
                taken_tools.remove(tool)
            elif matrix2.count(['1']) == 3:
                matrix2[0] = tool
                matrix2[1] = tool
                matrix2[2] = tool
                taken_tools.remove(tool)

        if tool in tools_slot2:
            if matrix0.count(['1']) == 2:
                matrix0[1] = [tool]
                matrix0[2] = [tool]
                taken_tools.remove(tool)
            elif matrix1[0] == ['1'] and matrix1[1] == ['1']:
                matrix1[0] = [tool]
                matrix1[1] = [tool]
                taken_tools.remove(tool)
            elif matrix1[1] == ['1'] and matrix1[2] == ['1']:
                matrix1[2] = [tool]
                matrix1[1] = [tool]
                taken_tools.remove(tool)
            elif matrix2[0] == ['1'] and matrix2[1] == ['1']:
                matrix2[0] = [tool]
                matrix2[1] = [tool]
                taken_tools.remove(tool)
            elif matrix2[1] == ['1'] and matrix2[2] == ['1']:
                matrix2[2] = [tool]
                matrix2[1] = [tool]
                taken_tools.remove(tool)

        if tool in tools_slot1:
            if matrix0.count(['1']) > 0:
                matrix0[matrix0.index(['1'])] = [tool]
                taken_tools.remove(tool)
            elif matrix1.count(['1']) > 0:
                matrix1[matrix1.index(['1'])] = [tool]
                taken_tools.remove(tool)
            elif matrix2.count(['1']) > 0:
                matrix2[matrix2.index(['1'])] = [tool]
                taken_tools.remove(tool)

print(f"{matrix0}\n{matrix1}\n{matrix2}")
print(surviving_points)
print(f"Набор предметов для задачи в семь ячеек:{get_tools_list(toolsdict,6)}")
print("Т.е. эта та же матрица выше, но без двух элементов 's'\nТогда очков выживания всего -10, т.е. при инвентаре в 7 ячеек даже при самом выгодном наборе Том не сможет выжить")
