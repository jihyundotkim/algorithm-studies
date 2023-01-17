def solution(storey):
    if type(storey) is not int:
        raise ValueError("층은 정수여야 합니다.")
    if storey < 1 or storey > 100000000:
        raise ValueError("1층 이상 100,000,000 이하를 입력하세요.")
    pisos = str(storey)
    pos = 0
    buttons = {}
    for digit in pisos[::-1]:
        digit = int(digit)
        if digit < 5:
            if f'10^{pos}' in buttons.keys():
                buttons[f'10^{pos}'] += digit
            else:
                buttons[f'10^{pos}'] = digit
        else:
            if f'10^{pos + 1 }' in buttons:
                buttons[f'10^{pos + 1}'] += 1
            else:
                buttons[f'10^{pos + 1}'] = 1
            buttons[f'-10^{pos}'] = 10 - digit
        pos += 1
    def neutralize_posneg(dictionary):
        negatives = [key for key in dictionary.keys() if key[0] == '-']
        for neg in negatives:
            positive_key = neg[1:]
            if positive_key in dictionary.keys():
                if dictionary[neg] >= dictionary[positive_key]:
                    dictionary[neg] = dictionary[neg] - dictionary[positive_key]
                    dictionary.pop(positive_key)
                elif dictionary[positive_key] > dictionary[neg]:
                    dictionary[positive_key] = dictionary[positive_key] - dictionary[neg]
                    dictionary.pop(neg)
        return dictionary

    buttons = neutralize_posneg(buttons)
    need_recalibration = [val for val in buttons.values() if val > 5]
    while need_recalibration:

        for key, val in buttons.items():
            if val > 5:
                buttons[key] = 10 - val
                if key[0:-1]+str(int(key[-1]) + 1) in buttons.keys():
                    buttons[key[0:-1]+str(int(key[-1]) + 1)] = buttons[key[0:-1]+str(int(key[-1]) + 1)] + 1
                else:
                    buttons[key[0:-1]+str(int(key[-1]) + 1)] = 1
                    break
                neutralize_posneg(buttons)
        
        need_recalibration = [val for val in buttons.values() if val > 5]
    
    neutralize_posneg(buttons)
    print(buttons)

    return int(sum(buttons.values()))