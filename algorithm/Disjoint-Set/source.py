"""
Build Disjoint Set
"""


class DisjointSet:
    def __init__(self, data: list, mode: str = "size"):
        """ Object Initialization

        :param data: a 1D list that need to stored in this Disjoint list
        :param mode: it decides what will be stored in parent array and how union work. (size/height)
        """
        self.index_data = self.generate_data_index(data)
        self.parent_array = [-1 for _ in range(len(data))]
        self.mode = mode

    @staticmethod
    def generate_data_index(data):
        """ Create a dictionary to store data and its index for later reference

        :param data: a 1d list data
        :return: a dictionary object stored the data and its index
        """
        result = {}
        for i in range(len(data)):
            result[data[i]] = i
        return result

    def find(self, item: int):
        """ Find the root of the tree containing the input item

        :param item: a node item may exist in the tree
        :return: the value of root item of the subtree/subset
        """
        assert item in self.index_data.keys(), "Input item is not existed in this Disjoint Set"
        flag = True
        current = item
        while flag:
            index = self.index_data[current]
            if self.parent_array[index] >= 0:
                current = self.parent_array[index]
            else:
                return current

    def union(self, item_1: int, item_2: int):
        """ Union the root node of the tree with smaller number of
            elements to the root for the larger one

        :param item_1: the value of a node item
        :param item_2: the value of a node item
        :return: None
        """
        def union_by_height():
            if value_1 <= value_2:
                self.parent_array[index_2] = root_1
                self.parent_array[index_1] -= 1
            else:
                self.parent_array[index_1] = root_2
                self.parent_array[index_2] -= 1

        def union_by_size():
            if value_1 <= value_2:
                self.parent_array[index_2] = root_1
                self.parent_array[index_1] = -(abs(value_1) + abs(value_2))
            else:
                self.parent_array[index_1] = root_2
                self.parent_array[index_2] = -(abs(value_1) + abs(value_2))

        root_1 = self.find(item_1)
        root_2 = self.find(item_2)

        assert root_1 != root_2, "Unionised items are located in the same tree"
        index_1 = self.index_data[root_1]
        index_2 = self.index_data[root_2]

        value_1 = self.parent_array[index_1]
        value_2 = self.parent_array[index_2]

        if self.mode == "height":
            union_by_height()
        else:
            union_by_size()


if __name__ == "__main__":
    data = [0, 1, 2, 3, 4, 5, 6, 7]
    disjoint_set = DisjointSet(data, "height")
    disjoint_set.union(4, 5)
    disjoint_set.union(6, 7)
    disjoint_set.union(5, 7)
    disjoint_set.union(3, 7)
    print(disjoint_set.parent_array)


