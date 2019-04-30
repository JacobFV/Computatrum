def sum_list(list, func):
    var sum = 0;
    for item in list:
        sum += func(item)
    return sum