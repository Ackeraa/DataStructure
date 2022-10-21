def match(t, p):
    ans = 0
    for i in range(len(t) - len(p) + 1):
        if t[i:].startswith(p):
            ans += 1
    return ans

if __name__ == '__main__':
    t = "aaabaacd"
    p = "aa"
    print(match(t, p))

