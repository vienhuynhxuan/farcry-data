def calculate_serial_killers(frags):
    longest_kill = {}
    temp = {}
    for frag in frags:
        if frag[2] not in longest_kill:
            longest_kill[frag[2]] = [(frag[1], frag[3], frag[4])]
        elif last_killer == frag[2]:
            longest_kill[frag[2]].append((frag[1], frag[3], frag[4]))
        else 
            if len(longest_kill[frag[2]]) > 1:
                temp[frag[2]] = longest_kill[frag[2]]
        last_killer = frag[0]

    for key, value in temp.items():
        if len(longest_kill[key]) < len(value):
            longest_kill[key] = value

    return longest_kill         