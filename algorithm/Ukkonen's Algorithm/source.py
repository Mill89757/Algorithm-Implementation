"""
Implement Ukkonen's suffix tree algorithm
Reference article: https://stackoverflow.com/questions/9452701/ukkonens-suffix-tree-algorithm-in-plain-english
"""
from __future__ import annotations


class Node:
    """ The Suffix-tree's Node"""

    def __init__(self, start: int = None, end: int = None):
        self.children = {}
        self.start_index = start
        self.end_index = end
        self.suffix_link_node = None
        self.is_leaf_node = True
        self.is_root_node = False

    def __len__(self):
        return (self.end_index - self.start_index) + 1 if self.end_index else 1

    def add_edge(self, key: str, new_node: Node):
        self.children[key] = new_node

    def extend_edge(self, pos: int):
        """ Extend the end position fot this node

        :param pos: an integer value represents value
        :return: None
        """
        self.end_index = pos

    def get_edges(self):
        """ Get all the edges extended from this node

        :return: a dict_keys object include all the first letter of extended edge
        """
        return self.children.keys()

    def get_connected_nodes(self):
        """ Get all the nodes connected from this node

        :return: a dict_values include all the connected Node object
        """
        return self.children.values()

    def get_node(self, character: str):
        """ Get a specific node from the connected nodes depending on its edge

        :param character: a lowercase letter which is the first letter of extended edge
        :return: a node object
        """
        return self.children[character]

    def update_node(self, character: str, new_node: Node):
        """ Update a node object for an extended edge

        :param character: a lowercase letter which is the first letter of extended edge
        :param new_node: a new node object
        :return: None
        """
        self.children[character] = new_node

    def update_suffix_link_node(self, new_node: Node):
        """ Update the node which is pointed by suffix link

        :param new_node: a node object
        :return: None
        """
        self.suffix_link_node = new_node


class SuffixTree:
    """ The Suffix-Tree """

    def __init__(self, text: str):
        self._text = text
        self.active_node = None
        self.active_edge = ""
        self.active_length = 0
        self.remainder = 1
        self.leaf_end = None
        self.size = -1
        self.root = None

    def build_tree(self):
        self.size = len(self._text)
        self.root = Node(0)
        self.root.is_root_node = True
        self.active_node = self.root

        # Implement steps in Ukkonen's algorithm
        for i in range(self.size):
            updated_active_point = False
            inserted_node = None
            # update the end index for most of edges
            if self.active_node.get_edges():
                self.leaf_end = i
            if self.remainder > 0:
                current_character = self._text[i]
                if self.remainder > 1 and self.active_edge != "":
                    # implement additional insert
                    remainder_count = self.remainder
                    for _ in range(remainder_count, 1, -1):
                        end_node = self.active_node.get_node(self.active_edge)
                        start_index = max(0, end_node.start_index - len(self.active_node))
                        current_index = start_index+self.active_length
                        if (self._text[current_index] == current_character and self.active_node == self.root)\
                                or (self.active_node != self.root and
                                    self._text[current_index+len(self.active_node)] == current_character):
                            if (not end_node.is_leaf_node) and self._text[end_node.end_index] == current_character:
                                self.active_node = self.active_node.get_node(self.active_edge)
                                self.active_edge = ""
                                self.active_length = 0
                                self.remainder += 1
                            else:
                                self.active_length += 1
                            updated_active_point = True
                            break
                        else:
                            # create an inner node and insert it into current tree
                            inner_node = self.insert(end_node, current_character, i)

                            has_split = True
                            self.remainder -= 1

                            # implement Rule - 2
                            """
                            If we split an edge and insert a new node, and if that is not the first node
                            created during the current step, we connect the previously inserted node and 
                            the new node through a special pointer, a suffix link. 
                            """
                            if inserted_node:
                                inserted_node.update_suffix_link_node(inner_node)
                            inserted_node = inner_node

                        # implement Rule - 1
                        """
                        After an insertion from root, active_node remains root,
                        active_edge is set to the first character of the new suffix we need to insert.
                        """
                        if self.active_node == self.root and has_split:
                            self.active_edge = self._text[i-self.remainder+1]
                            self.active_length -= 1

                        # implement Rule - 3
                        """
                        After splitting an edge from an active_node that is not the root node, we follow 
                        the suffix link going out of that node, if there is any, and reset the active_node 
                        to the node it points to. If there is no suffix link, we set the active_node to the
                        root. active_edge and active_length remain unchanged.
                        """
                        if self.active_node != self.root and has_split:
                            if self.active_node.suffix_link_node:
                                self.active_node = self.active_node.suffix_link_node
                            else:
                                self.active_node = self.root

                # normal insertion for each step
                if current_character in self.active_node.get_edges():
                    # the character has existed in the current node's children
                    # update the active point
                    if not updated_active_point:
                        self.active_edge, self.active_length = current_character, 1
                    self.remainder += 1
                else:
                    if not updated_active_point:
                        self.active_node.add_edge(current_character, Node(i))

    def insert(self, current_end_node: Node, new_edge: str, new_edge_index: int):
        """ Insert a new node into this suffix tree

        :param current_end_node: the previous node that connected with parent node
        :param new_edge: the new edge that will be extended from the new inner node
        :param new_edge_index: the index of first letter of new edge
        :return: the new generated inner node which can be used to add suffix link
        """
        # create and update node info
        inner_node = Node(current_end_node.start_index, current_end_node.start_index + self.active_length - 1)
        current_end_node.start_index = current_end_node.start_index + self.active_length
        new_node = Node(new_edge_index)

        # update node connections
        inner_node.is_leaf_node = False
        self.active_node.update_node(self._text[inner_node.start_index], inner_node)
        inner_node.add_edge(self._text[current_end_node.start_index], current_end_node)
        inner_node.add_edge(new_edge, new_node)

        return inner_node

    def get_substring(self, node: Node):
        """ Generate the substring object for a specific node depending on its position

        :param node: a suffix tree node
        :return: a non-empty string object
        """
        if node.is_leaf_node:
            return self._text[node.start_index:]
        else:
            return self._text[node.start_index:node.end_index+1]

    def match_pattern(self, pattern: str):
        """ Find out the pattern is existed in this suffix tree or not

        :param pattern: a non-empty string which is only made of lowercase letters
        :return: return true if it is existed, otherwise return false
        """
        return self.match_pattern_aux(self.root, pattern)

    def match_pattern_aux(self, parent_node: Node, pattern: str):
        if parent_node.is_leaf_node and (not parent_node.is_root_node):
            substring = self.get_substring(parent_node)
        else:
            try:
                child_node = parent_node.get_node(pattern[0])
                substring = self.get_substring(child_node)
            except KeyError:
                return False
        mini_length = min(len(pattern), len(substring))
        for i in range(mini_length):
            if pattern[i] != substring[i]:
                return False
        if mini_length < len(pattern):
            return True and self.match_pattern_aux(child_node, pattern[mini_length:])
        else:
            return True

    def traversing(self, current: Node, prefix: str = ""):
        """ Print out all the suffix existed in this suffix tree

        :param current: the current parent node
        :param prefix: a substring which may generated by inner node
        :return: None
        """
        for end_node in current.get_connected_nodes():
            if end_node.get_connected_nodes():
                new_prefix = self._text[end_node.start_index:end_node.end_index+1]
                self.traversing(end_node, prefix+new_prefix)
            else:
                start = end_node.start_index
                if end_node.end_index:
                    print(prefix+self._text[start:end_node.end_index+1])
                else:
                    print(prefix+self._text[start:])


if __name__ == "__main__":
    content = "abcabxabcd"
    content = "aabbaabb"
    suffix_tree = SuffixTree(content)
    suffix_tree.build_tree()
    suffix_tree.traversing(suffix_tree.root)
    # print(suffix_tree.match_pattern("abxa"))
    # print(suffix_tree.match_pattern("cabxabcdd"))
