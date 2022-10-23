"""
Implement pattern matching

"""


def naive_algorithm(pattern: str, text: str) -> int:
    """ Simply find the pattern in the target word

    Arg:
        :param text: the substring that need to be matched
        :param pattern: the original string
    Rtn:
        :return: the index of first occurrence of pattern

    Time complexity (Worst Case): P(mn)
    """
    n = len(text)
    m = len(pattern)
    for i in range(n-m+1):
        for j in range(m):
            if text[i+j] != pattern[j]:
                break
        if j+1 == m:
            return i


def z_algorithm(pattern: str, text: str) -> int:
    """ Implement Gusfield's Z-algorithm to find the
        first occurrence of input substring. "$" is used
        as the combined operator in this case.

    Arg:
        :param text: the substring with length >= 2
        :param pattern: the original string
    Rtn:
        :return: the index of first occurrence of pattern

    Time complexity (Worst Case): P(m+n)
    """
    n = len(text)
    m = len(pattern)
    concatenated_str = pattern + "$" + text
    length = m + n + 1

    z_values = [0 for _ in range(length)]
    l, r = 0, 0
    k = 1
    while k < length:
        # Case 1
        if k > r:
            z_k = 0
            for i in range(length-k):
                if concatenated_str[i] != concatenated_str[k+i]:
                    break
                else:
                    z_k += 1
            if z_k > 0:
                l, r = k, k + z_k - 1
                z_values[k] = z_k
        else:
            # Case 2a
            if z_values[k-l] < r-k+1:
                z_values[k] = z_values[k-l+1]
            # Case 2b
            else:
                assert z_values[k-l] >= r-k+1, "Z value is too small in Z algorithm Case 2b"
                z_k = z_values[k-l]
                for i in range(length-r-1):         # operation with length value and index value
                    if concatenated_str[r+1+i] != concatenated_str[r-k+1+i]:
                        break
                    else:
                        z_k += 1
                z_values[k] = z_k
                l, r = k, k + z_k - 1
        k += 1

    # Find out the first occurrence
    for i, z_value in enumerate(z_values):
        if z_value == m:
            return i - 1 - m


if __name__ == "__main__":
    word = "bbabaxababay"
    target = "aba"
    word = "sdafffsdffqewrfqewrdsf;lrewjgkregnkngjkjfdkhgjklrem,gfdjkhgbjkfdhbjkbnruigfiu2tqrqwr"
    target = "wrfqewrdsf;lrewjgkregnkngjkjfd"
    index = z_algorithm(target, word)
    print(index)
    assert word[index:index+len(target)] == target, "Failed"
