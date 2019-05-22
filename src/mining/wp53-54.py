def calculate_serial_killers(frags):
    longest_kill = {}
    temp = {}
    label_last_lose = []   

    for frag in frags:
        if len(frag) == 4:
            if frag[2] in longest_kill and frag[2] not in label_last_lose:
                label_last_lose.append(frag[2])
            if frag[1] not in longest_kill:
                longest_kill[frag[1]] = [(frag[0], frag[2], frag[3])]
            elif frag[1] not in label_last_lose:
                longest_kill[frag[1]].append((frag[0], frag[2], frag[3]))
            else:
                temp[frag[1]] = longest_kill[frag[1]]
                longest_kill[frag[1]] = [(frag[0], frag[2], frag[3])]                
                label_last_lose.remove(frag[1])

    for key, value in temp.items():
        if len(longest_kill[key]) < len(value):
            longest_kill[key] = value
    return longest_kill         


def calculate_serial_losers(frags):
    longest_lose = {}
    temp = {}
    label_last_kill = []   

    for frag in frags:
        if len(frag) == 4:
            if frag[1] in longest_lose and frag[1] not in label_last_kill:
                label_last_kill.append(frag[1])
            if frag[2] not in longest_lose:
                longest_lose[frag[1]] = [(frag[0], frag[1], frag[3])]
            elif frag[2] not in label_last_kill:
                longest_kill[frag[1]].append((frag[0], frag[1], frag[3]))
            else:
                temp[frag[2]] = longest_kill[frag[1]]
                longest_kill[frag[2]] = [(frag[0], frag[1], frag[3])]                
                label_last_kill.remove(frag[2])

    for key, value in temp.items():
        if len(longest_kill[key]) < len(value):
            longest_kill[key] = value
    return longest_kill         


def calculate_lucky_luke_killers()