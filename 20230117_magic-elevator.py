# 마법의 세계에 사는 민수는 아주 높은 탑에 살고 있습니다. 탑이 너무 높아서 걸어 다니기 힘든 민수는 마법의 엘리베이터를 만들었습니다. 마법의 엘리베이터의 버튼은 특별합니다. 마법의 엘리베이터에는 -1, +1, -10, +10, -100, +100 등과 같이 절댓값이 10c (c ≥ 0 인 정수) 형태인 정수들이 적힌 버튼이 있습니다. 마법의 엘리베이터의 버튼을 누르면 현재 층 수에 버튼에 적혀 있는 값을 더한 층으로 이동하게 됩니다. 단, 엘리베이터가 위치해 있는 층과 버튼의 값을 더한 결과가 0보다 작으면 엘리베이터는 움직이지 않습니다. 민수의 세계에서는 0층이 가장 아래층이며 엘리베이터는 현재 민수가 있는 층에 있습니다.

# 마법의 엘리베이터를 움직이기 위해서 버튼 한 번당 마법의 돌 한 개를 사용하게 됩니다.예를 들어, 16층에 있는 민수가 0층으로 가려면 -1이 적힌 버튼을 6번, -10이 적힌 버튼을 1번 눌러 마법의 돌 7개를 소모하여 0층으로 갈 수 있습니다. 하지만, +1이 적힌 버튼을 4번, -10이 적힌 버튼 2번을 누르면 마법의 돌 6개를 소모하여 0층으로 갈 수 있습니다.

# 마법의 돌을 아끼기 위해 민수는 항상 최소한의 버튼을 눌러서 이동하려고 합니다. 민수가 어떤 층에서 엘리베이터를 타고 0층으로 내려가는데 필요한 마법의 돌의 최소 개수를 알고 싶습니다. 민수와 마법의 엘리베이터가 있는 층을 나타내는 정수 storey 가 주어졌을 때, 0층으로 가기 위해 필요한 마법의 돌의 최소값을 return 하도록 solution 함수를 완성하세요.


def solution(storey):
    # 우선 제한사항에 맞지 않는 것들은 오류 처리합니다.
    if type(storey) is not int:
        raise ValueError("층은 정수여야 합니다.")
    if storey < 1 or storey > 100000000:
        raise ValueError("1층 이상 100,000,000 이하를 입력하세요.")

    # 편의상 문자열로 바꿔서 썼습니다.
    pisos = str(storey)
    pos = 0

    # 1의 자리부터 6 이상은 더 높은 버튼을 누르고 빼는 것으로 처리하고
    # 5 이하의 수는 그대로 쓰는 것으로 합니다.
    buttons = {}     # 어떤 버튼을 얼마나 누르는지 딕셔너리에 저장합니다.
    for digit in pisos[::-1]:    # 1의 자리부터 시작하기 위해 ::-1로 슬라이스해서 순서를 뒤집었습니다.
        digit = int(digit)    # 문자로 바꿨으니까 다시 정수로...
        if digit < 5:
            # 이미 딕셔너리에 있는 버튼의 경우 더하고 딕셔너리에 없으면 새로 추가합니다.
            if f'10^{pos}' in buttons.keys():
                buttons[f'10^{pos}'] += digit
            else:
                buttons[f'10^{pos}'] = digit
        else:
            if f'10^{pos + 1 }' in buttons:
                buttons[f'10^{pos + 1}'] += 1
            else:
                buttons[f'10^{pos + 1}'] = 1
            buttons[f'-10^{pos}'] = 10 - digit # 마이너스 버튼은 10에서 뺀 만큼 눌러야 하겠죠
        pos += 1
    
    # 같은 지수에서 +와 - 버튼이 중첩될 필요가 없으므로 값이 큰 쪽에서 작은 쪽을 뺄셈하여 일원화합니다.
    # 여러 번 쓸 것 같아 함수로 만들었습니다.
    def neutralize_posneg(dictionary):
        # 우선 - 버튼을 모두 불러옵니다
        negatives = [key for key in dictionary.keys() if key[0] == '-']
        for neg in negatives:
            positive_key = neg[1:]
            # 겹치는 + 버튼이 있는 경우만 처리합니다.
            if positive_key in dictionary.keys():
                if dictionary[neg] > dictionary[positive_key]:
                    dictionary[neg] = dictionary[neg] - dictionary[positive_key]
                    dictionary.pop(positive_key)
                elif dictionary[positive_key] >= dictionary[neg]:
                    dictionary[positive_key] = dictionary[positive_key] - dictionary[neg]
                    dictionary.pop(neg)
        return dictionary

    # 우선 한 번 정리해주고...
    buttons = neutralize_posneg(buttons)
    # 값이 5였는데 10^n이 6 이상이어서 10^n+1에 1을 더하고
    # -10^n 버튼을 필요한 만큼 누르는 것으로 처리한 경우 다시 6 이상이 될 수 있습니다.
    # 이것을 다시 정리합니다.
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
        # need_recalibration이 빈 리스트가 되어서 false-y 해질 경우 while이 끝나게 됩니다.
    
    neutralize_posneg(buttons)
    # 한번 더 정리해줍니다.


    # 마지막으로 눌러야 하는 버튼 수를 총합하여 리턴합니다.
    return int(sum(buttons.values()))


# 문제 출처: 프로그래머스 "마법의 엘리베이터"
# https://school.programmers.co.kr/learn/courses/30/lessons/148653
# 제출 결과는 Test 6, Test 9가 실패 처리되어 84.6점인데 뭐가 문제라서 실패하는지 잘 모르겠습니다...
# 리뷰해주시고 고칠 부분을 알려주시면 감사하겠습니다.