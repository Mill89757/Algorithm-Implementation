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


class GusfieldZ:
    def __init__(self, text: str, pattern: str = None):
        self.pattern = pattern
        self.text = text
        self.concatenated_str = None
        self.z_values = None

    def generate_z_values(self) -> list:
        assert self.concatenated_str is not None, "The pattern is empty"
        length = len(self.concatenated_str)
        z_values = [0 for _ in range(length)]
        l, r = 0, 0
        k = 1
        while k < length:
            # Case 1
            if k > r:
                z_k = 0
                for i in range(length - k):
                    if self.concatenated_str[i] != self.concatenated_str[k + i]:
                        break
                    else:
                        z_k += 1
                if z_k > 0:
                    l, r = k, k + z_k - 1
                    z_values[k] = z_k
            else:
                # Case 2a
                if z_values[k - l] < r - k + 1:
                    z_values[k] = z_values[k - l]
                # Case 2b
                else:
                    assert z_values[k - l] >= r - k + 1, "Z value can not be increased since its value is too small"
                    z_k = z_values[k - l]
                    if z_values[k-l] + k > length:
                        z_k = length - k
                    else:
                        for i in range(length - r - 1):  # operation with length value and index value
                            if self.concatenated_str[r + 1 + i] != self.concatenated_str[r - k + 1 + i]:
                                break
                            else:
                                z_k += 1
                    z_values[k] = z_k
                    l, r = k, k + z_k - 1
            k += 1
        return z_values

    def find(self, pattern: str):
        """ Implement Gusfield's Z-algorithm to find the
        first occurrence of input substring. "$" is used
        as the combined operator in this case.

        Arg:
            :param pattern: the original string
        Rtn:
            :return: the index of first occurrence of pattern

        Time complexity (Worst Case): P(m+n)
        """
        self.pattern = pattern
        m = len(pattern)
        self.concatenated_str = self.pattern + "$" + self.text
        self.z_values = self.generate_z_values()

        # Find out the first occurrence
        for i, z_value in enumerate(self.z_values):
            if z_value == m:
                return i - 1 - m


if __name__ == "__main__":
    word = "bbabaxababay"
    target = "aba"
    word = "sdafffsdffqewrfqewrdsf;lrewjgkregnkngjkjfdkhgjklrem,gfdjkhgbjkfdhbjkbnruigfiu2tqrqwr"
    target = "lrewjgkregnkngjkjfd"
    p_gz = GusfieldZ(word, "acababacaba")
    # index = p_gz.find(target)
    p_gz.concatenated_str = "acababacaba"
    print(p_gz.generate_z_values())
    # assert word[index:index+len(target)] == target, "Failed"
