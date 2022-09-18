def split_to_consecutive_streaks(s):
    if not len(s):
        return []
    result = []
    substring = s[0]
    for c in s[1:]:
        if c == substring[0]:
            substring += c
        else:
            result.append(substring)
            substring = c
    result.append(substring)
    return result
