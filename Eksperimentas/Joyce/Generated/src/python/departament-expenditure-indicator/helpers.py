from heapq import heappush, heappop
import operator

def calculate_median(new_element, lowers, highers):
    add_number(new_element, lowers, highers)
    rebalance(lowers, highers)
    return get_median(lowers, highers)

def calculate_mean(total, count):
    return total/count

def calculate_mode(new_element, element_dict):
    rounded_element = round(new_element, 2)
    if rounded_element in element_dict:
        element_dict[rounded_element] = element_dict[rounded_element] + 1
    else:
        element_dict[rounded_element] = 1
    result = max(element_dict.items(), key=operator.itemgetter(1))[0]
    if result == 1:
        return -1
    return result

def add_number(number, lowers, highers):
    if not highers or number > highers[0]:
        heappush(highers, number)
    else:
        heappush(lowers, -number)  # for lowers we need a max heap

def rebalance(lowers, highers):
    if len(lowers) - len(highers) > 1:
        heappush(highers, -heappop(lowers))
    elif len(highers) - len(lowers) > 1:
        heappush(lowers, -heappop(highers))

def get_median(lowers, highers):
    if len(lowers) == len(highers):
        return (-lowers[0] + highers[0])/2
    elif len(lowers) > len(highers):
        return -lowers[0]
    else:
        return highers[0]

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

