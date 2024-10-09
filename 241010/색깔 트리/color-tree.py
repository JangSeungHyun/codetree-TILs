# 
class Node:
    def __init__(self, m_id, p_id, color, max_depth):
        self.m_id = m_id
        self.p_id = p_id
        self.color = color
        self.max_depth = max_depth
        self.child = []

    def change_color(self, color):
        self.color = color

    def retrieve_color(self):
        return self.color


class Tree:
    def __init__(self):
        self.root = Node(-1, -1, 0, 20000)
        self.node_dict = {-1: self.root}  # Dictionary to store nodes by m_id for O(1) access

    def find_node(self, m_id):
        return self.node_dict.get(m_id)

    def find_height(self, node):
        if not node.child:
            return 1
        return 1 + max(self.find_height(child) for child in node.child)

    def add_node(self, m_id, p_id, color, max_depth):
        parent_node = self.find_node(p_id)
        if not parent_node:
            return  # parent doesn't exist
        if self.find_height(parent_node) >= parent_node.max_depth:
            return  # exceeds max depth

        new_node = Node(m_id, p_id, color, max_depth)
        parent_node.child.append(new_node)
        self.node_dict[m_id] = new_node

    def change_node_color(self, m_id, color):
        node = self.find_node(m_id)
        if not node:
            return

        def change_color_subtree(node, color):
            node.change_color(color)
            for child in node.child:
                change_color_subtree(child, color)

        change_color_subtree(node, color)

    def find_color(self, m_id):
        node = self.find_node(m_id)
        if node:
            print(node.retrieve_color())

    def return_values(self):
        def sub_func(node):
            if not node.child:
                return {node.color}, 1 ** 2

            total_value = 0
            color_set = set()
            for child in node.child:
                child_colors, child_value = sub_func(child)
                color_set.update(child_colors)
                total_value += child_value

            color_set.add(node.color)
            return color_set, total_value + len(color_set) ** 2

        total_value = 0
        for child in self.root.child:
            _, child_value = sub_func(child)
            total_value += child_value

        print(total_value)


def main():
    curr_tree = Tree()
    inst_num = int(input())

    for _ in range(inst_num):
        inst = input().split()
        cmd, *args = map(int, inst)
        
        if cmd == 100:
            curr_tree.add_node(args[0], args[1], args[2], args[3])
        elif cmd == 200:
            curr_tree.change_node_color(args[0], args[1])
        elif cmd == 300:
            curr_tree.find_color(args[0])
        elif cmd == 400:
            curr_tree.return_values()

if __name__ == '__main__':
    main()