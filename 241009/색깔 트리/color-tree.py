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
        self.root = None
    
    # m_id로 node 찾아서 리턴하는 함수
    def find_node(self, m_id):
        
        queue = list()
        queue.append(self.root)

        while len(queue) > 0:
            curr_node = queue.pop(0)

            if curr_node.m_id == m_id:
                return curr_node

            for node in curr_node.child:
                queue.append(node)


    def add_node(self, m_id, p_id, color, max_depth):

        # node의 height를 찾는 함수
        def find_height(node):
            
            max_height = 1
            curr_height = 1

            for child_node in node.child:
                if len(child_node.child) == 0:
                    curr_height = curr_height + 1
                else:
                    curr_height = find_height(child_node) + 1
                
                if max_height < curr_height:
                    max_height = curr_height
            
            return max_height 

        def find_node_and_stack(root: node, stack: list, p_id: int):
            
            stack.append(root)
            
            if root.m_id == p_id:
                return stack
            else:
                if len(root.child) == 0:
                    stack.pop(-1)
                    return stack
                else:
                    for node in root.child:
                        new_stack = find_node_and_stack(node, stack, p_id)
                        if stack[-1].m_id == p_id: # p_id == m_id인 노드 찾음
                            return new_stack
                        else:
                            stack.pop(-1)
                            return stack
                    

        # max depth 고려해야 -> root로 추가되면 모든 노드 점검, 아니라면 본인부터 올라가며 점검
        # 어떻게 parent node를 찾을까?
        if p_id == -1:
            if self.root == None: # 루트 새로 지정
                self.root = node(m_id, p_id, color, max_depth)
            else: # 루트 대체 필요 -> 새로운 루트의 max_depth와 height 비교필요
                if find_height(self.root) + 1 > self.root.max_depth:
                    return
                temp = self.root
                self.root = node(m_id, p_id, color, max_depth)
                self.root.child.append(temp)
        else: # max depth
            p_node = self.find_node(p_id)
            if len(p_node.child) != 0:
                p_node.child.append(node(m_id, p_id, color, max_depth))
            else:
                # 경로 stack 구성
                stack = list()
                stack = find_node_and_stack(self.root, stack, p_id)

                while len(stack) > 0:
                    curr_root = stack.pop(len(stack) - 1)
                    curr_root_height = find_height(curr_root)
                    
                    if curr_root_height + 1 > curr_root.max_depth:
                        return
                    else:
                        continue

                # print(p_id)
                # print(p_node)
                p_node.child.append(node(m_id, p_id, color, max_depth))

    # node의 subtree 모두 color 변경해야
    def change_node_color(self, m_id, color):

        def change_sub_tree(curr_root_node, color):
            curr_root_node.change_color(color)
            if len(curr_root_node.child) != 0:
                for child in curr_root_node.child:
                    change_sub_tree(child, color)
                return
            else:
                return

        curr_root = self.find_node(m_id)
        change_sub_tree(curr_root, color)

    def find_color(self, m_id):
        
        target_node = self.find_node(m_id)
        # def curr_node_color(curr_root_node, m_id):
        #     if curr_root_node.m_id == m_id:
        #         return curr_root_node.retrieve_color()
        #     else:
        #         if curr_root_node.child != None:
        #             for child in curr_root_node.child:
        #                 result_color = curr_node_color(child, m_id)
        #                 if result_color is not None:
        #                     break

        #             return result_color
        #         else:
        #             return None
        
        print(target_node.retrieve_color())
    
    
    def return_values(self):

        def retrieve_subtree_num_colors(curr_root, color_set):
            color_set.add(curr_root.color)
            
            if len(curr_root.child) > 0:
                for node in curr_root.child:
                    color_set = retrieve_subtree_num_colors(node, color_set)
                
            return color_set

        queue = list()
        queue.append(self.root)
        total_value = 0

        while len(queue) > 0:
            curr_root = queue.pop(0)
            for node in curr_root.child:
                queue.append(node)
            
            color_set = set([])
            num_color = len(retrieve_subtree_num_colors(curr_root, color_set))
            total_value += num_color ** 2

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