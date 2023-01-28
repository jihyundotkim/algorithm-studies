# https://www.acmicpc.net/problem/10250

PYTHONDONTWRITEBYTECODE = "false"
import sys
import re
import math

regex = re.compile(r"\d+")
for line in sys.stdin:
    if line.find(" ") == -1:
        continue # 첫줄은 패스
    else:
        args = regex.findall(line)
        h = int(args[0])
        w = int(args[1])
        n = int(args[2])
        if n % h > 0:
            room = f"{n % h}{math.ceil(n / h):02d}"
        elif n < h:
            room = f"{n}01"
        else:
            room = f"{h}{math.ceil(n / h):02d}"
        print(room)