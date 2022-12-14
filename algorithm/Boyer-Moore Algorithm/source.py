"""
Implement pattern matching solution
Boyer-Moore Algorithm

"""


def generate_z_values(pattern: str) -> list:
    length = len(pattern)
    z_values = [0 for _ in range(length)]
    l, r = 0, 0
    k = 1
    while k < length:
        # Case 1
        if k > r:
            z_k = 0
            for i in range(length - k):
                if pattern[i] != pattern[k + i]:
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
                if z_values[k - l] + k > length:
                    z_k = length - k
                else:
                    for i in range(length - r - 1):  # operation with length value and index value
                        if pattern[r + 1 + i] != pattern[r - k + 1 + i]:
                            break
                        else:
                            z_k += 1
                z_values[k] = z_k
                l, r = k, k + z_k - 1
        k += 1
    return z_values


class BoyerMoore:
    def __init__(self, text: str, pattern: str = None):
        self.text = text
        self.pattern = pattern
        self.bad_character_matrix = None
        self.z_suffix = None
        self.good_suffix = None
        self.matched_prefix = None

    def generate_bad_character(self) -> list:
        assert self.pattern is not None, "The pattern is empty"
        m = len(self.pattern)
        result = []
        for i in range(m):
            if i == 0:
                result.append([0 for _ in range(26)])
            else:
                current_record = result[-1]
                position = ord(self.pattern[i - 1]) - 97    # ascii lowercase start from 97
                new_record = [item for item in current_record]
                new_record[position] = i-1
                result.append(new_record)
        return result

    def generate_z_suffix(self) -> list:
        assert self.pattern is not None, "The pattern is empty"
        pattern = self.pattern[::-1]
        z_values = generate_z_values(pattern)
        return z_values[::-1]

    def generate_good_suffix(self) -> list:
        assert self.pattern is not None, "The pattern is empty"
        m = len(self.pattern)
        values = [0 for _ in range(m+1)]
        for position in range(m-1):
            index = m - self.z_suffix[position]
            values[index] = position + 1
        return values

    def generate_matched_prefix(self) -> list:
        assert self.pattern is not None, "The pattern is empty"
        z_values = generate_z_values(self.pattern)
        length = len(z_values)
        matched_prefix = [0 for _ in range(length)]
        matched_prefix[-1] = len(self.pattern)
        longest_prefix_length = 1 if self.pattern[0] == self.pattern[-1] else 0
        for i in range(length-1, 0, -1):
            if z_values[i] > longest_prefix_length and z_values[i] == i - 1:
                longest_prefix_length = z_values[i]
            matched_prefix[length-i-1] = longest_prefix_length
        return matched_prefix[::-1]+[0]

    def get_next_shift(self, index: int, counter: int) -> int:
        m = len(self.pattern)
        character = self.pattern[index]
        bad_character_shift = m - self.bad_character_matrix[counter][ord(character)-97] - 1
        if self.good_suffix[index+1] != 0:
            good_suffix_shift = m - self.good_suffix[index+1] - 1
        else:
            good_suffix_shift = m - self.matched_prefix[index+1] - 1
        return max(bad_character_shift, good_suffix_shift)

    def find(self, pattern: str) -> int:
        """ Implement Boyer-Moore Algorithm to find the
                first occurrence of input substring. The text only contains
                LOWERCASE letter in this case

            Arg:
                :param pattern: the substring of the original string
            Rtn:
                :return: the index of first occurrence of pattern
            Time Complexity (Worst case): O(M+N)
        """
        # Preprocessing
        self.pattern = pattern
        self.bad_character_matrix = self.generate_bad_character()
        self.z_suffix = self.generate_z_suffix()
        self.good_suffix = self.generate_good_suffix()
        self.matched_prefix = self.generate_matched_prefix()

        print(self.bad_character_matrix)
        print(self.z_suffix)
        print(self.good_suffix)
        print(self.matched_prefix)
        m, n = len(self.pattern), len(self.text)

        # Implement Galil's Optimization
        naive_shift = 1
        occurrence = []
        j = 0
        stop_point = -1
        while j < n - m + 1:
            mismatched_index = None
            counter = m - 1
            for i in range(m-1, stop_point, -1):
                if self.pattern[i] != self.text[j+i]:
                    mismatched_index = i
                    stop_point = i-1
                    counter -= 1
                    break
            if mismatched_index is not None:
                if mismatched_index + 1 >= m:
                    break
                j += max(self.get_next_shift(mismatched_index+1, counter), naive_shift)
            else:
                occurrence.append(j)
                j += max(self.matched_prefix[0], naive_shift)
        return occurrence


if __name__ == "__main__":
    # text = "aaacababacabaabcabcabacababacababjdcn"
    # target = "acababacaba"
    # word = "sdafffsdffqewrfqewrdsf;lrewjgkregnkngjkjfdkhgjklrem,gfdjkhgbjkfdhbjkbnruigfiu2tqrqwr"
    # target = "wrfqewrdsf;lrewjgkregnkngjkjfd"
    # text = "tbapxabbbtbapxababtbapxabaxababay"
    # target = "tbapxab"
    # p_by = BoyerMoore(target, word)
    # print(p_by.generate_matched_prefix())
    print("Test")
    p_by = BoyerMoore(text)
    index = p_by.find(target)
    print(index)
    # assert text[index[0]:index[0] + len(target)] == target, "Failed"
