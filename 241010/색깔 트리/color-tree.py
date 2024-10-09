class node:
    
    def __init__(self, m_id, p_id, color, max_depth):
        self.m_id = m_id
        self.p_id = p_id
        self.color = color
        self.max_depth = max_depth
        self.child = list()

    def change_color(self, color):
        self.color = color
    
    def retrieve_color(self):
        return self.color


class tree:

    def __init__(self):
        self.root = node(-1, -1, 0, 20000)
    
    # m_id로 node 찾아서 리턴하는 함수
    def find_node(self, m_id):

        queue = list()
        for sub_root in self.root.child:

            queue.append(sub_root)

            while len(queue) > 0:
                curr_node = queue.pop(0)

                for node in curr_node.child:
                    queue.append(node)

                if curr_node.m_id == m_id:
                    return curr_node, sub_root
        
        # stack = list()
        # visited = list()

        # for sub_root in self.root.child:
        #     stack.append(sub_root)

        #     while stack:
        #         curr_node = stack.pop(-1)
        #         if curr_node.m_id not in visited:
        #             visited.append(curr_node.m_id)

        #             if curr_node.m_id == m_id:
        #                 return curr_node, sub_root

        #             if len(curr_node.child) == 0:
        #                 continue
        #             else:
        #                 for node in curr_node.child:
        #                     stack.append(node)
        #         else:
        #             continue


    # node의 height를 찾는 함수
    def find_height(self, node):
            
        max_height = 1
        curr_height = 1

        if len(node.child) == 0:
            max_height = 1
        else:
            for child_node in node.child:
                curr_height = self.find_height(child_node) + 1
                
                if max_height < curr_height:
                    max_height = curr_height
            
        return max_height 


    def find_node_and_stack(self, root: node, stack: list, p_id: int):
            
        stack.append(root)
            
        if root.m_id == p_id:
            return stack
        else:
            if len(root.child) == 0:
                stack.pop(-1)
                return stack
            else:
                for node in root.child:
                    new_stack = self.find_node_and_stack(node, stack, p_id)
                    if stack[-1].m_id == p_id: # p_id == m_id인 노드 찾음
                        return new_stack
                    else:
                        stack.pop(-1)
                        return stack

            
    def add_node(self, m_id, p_id, color, max_depth):

        if p_id == -1: # 새로운 트리 생성 필요
            self.root.child.append(node(m_id, p_id, color, max_depth))
        else: # max depth
            p_node, sub_root = self.find_node(p_id)
            if len(p_node.child) != 0:
                p_node.child.append(node(m_id, p_id, color, max_depth))
            else:
                curr_id = p_id
                while curr_id != -1:
                    curr_node, _ = self.find_node(curr_id)

                    if len(curr_node.child) != 0:
                        curr_id = curr_node.p_id
                        continue

                    curr_node_height = self.find_height(curr_node)

                    if curr_node_height + 1 > curr_node.max_depth:
                        return
                    else:
                        curr_id = curr_node.p_id
                        
                p_node.child.append(node(m_id, p_id, color, max_depth))


    # node의 subtree 모두 color 변경해야
    def change_node_color(self, m_id, color):
        
        curr_root, sub_root = self.find_node(m_id)

        queue = list()
        queue.append(curr_root)

        while len(queue) > 0:
            curr_node = queue.pop(0)
            for child_node in curr_node.child:
                queue.append(child_node)
            curr_node.change_color(color)


    def find_color(self, m_id):
        target_node, sub_root = self.find_node(m_id)
        print(target_node.retrieve_color())
    
    
    def return_values(self):

        def sub_func(sub_root: node, total_value: int, color_set: set):

            # 자식 노드 처리
            if len(sub_root.child) == 0:
                color_set.add(sub_root.color)
                total_value += 1**2
            else:
                curr_sub_colorset = set([])
                for child_of_sub_root in sub_root.child:
                    curr_sub_colorset, total_value = sub_func(child_of_sub_root, total_value, curr_sub_colorset)
                
                curr_sub_colorset.add(sub_root.color)
                total_value += len(curr_sub_colorset) ** 2
                color_set = color_set.union(curr_sub_colorset)

            return color_set, total_value

        total_value = 0

        for sub_root in self.root.child:
            color_set = set([])
            curr_sub_total_value = 0

            color_set, curr_sub_total_value = sub_func(sub_root, curr_sub_total_value, color_set)
            total_value += curr_sub_total_value

        print(total_value)

        return 


def main():
    curr_tree = tree()

    inst_num = int(input())

    for i in range(inst_num):
        inst = input().split()
        if inst[0] == '100': # 노드 추가
            curr_tree.add_node(int(inst[1]), int(inst[2]), int(inst[3]), int(inst[4]))
        elif inst[0] == '200': # 색깔 변경
            curr_tree.change_node_color(int(inst[1]), int(inst[2]))
        elif inst[0] == '300': # 색깔 조회
            curr_tree.find_color(int(inst[1]))
        elif inst[0] == '400': # 점수 조회
            curr_tree.return_values()

if __name__=='__main__':
    main()