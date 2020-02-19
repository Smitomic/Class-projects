from typing import List, Tuple, Optional


class Node:
    def __init__(self, name, owner, is_dir, size, parent, children):
        self.name = name
        self.owner = owner
        self.is_dir = is_dir
        self.size = size
        self.parent = parent
        self.children = children

    # uloha 2
    def validate_files_size(self: "Node", min_size: int) -> bool:
        a = True
        if self.is_dir:
            for child in self.children:
                a = a and child.validate_files_size(min_size)
        else:
            return self.size >= min_size
        return a

    def file_count(self: "Node") -> int:
        count = 0
        for child in self.children:
            if not child.is_dir:
                count += 1
        return count

    def validate_files_count(self: "Node", max_files: int) -> bool:
        files = self.file_count()
        final = files <= max_files
        if not final:
            return False
        for child in self.children:
            if child.is_dir:
                final = child.validate_files_count(max_files)
                if not final:
                    return False
        return True

    # uloha 3
    def check_children_user(self, user, check=True):
        for child in self.children:
            if child.owner == user:
                check = check and True
            else:
                check = False
            if child.is_dir:
                check = check and child.check_children_user(user, check)
        return check

    def child_belongings(self: "Node", user: str,
                         user_list: List["Node"]) -> None:
        for child in self.children:
            if (child.owner == user) and child.check_children_user(user):
                user_list.append(child)
            if child.is_dir:
                child.child_belongings(user, user_list)

    def all_belongs_to(self: "Node", user: str) -> List["Node"]:
        user_list = []
        if self.owner == user and self.check_children_user(user):
            user_list.append(self)
        self.child_belongings(user, user_list)
        return user_list

    def child_files(self: "Node", max_list: List[int],
                    node_list: List["Node"]) -> None:
        for child in self.children:
            max_list.append(self.file_count())
            node_list.append(self)
            if child.is_dir:
                child.child_files(max_list, node_list)

    def get_most_files(self: "Node") -> Optional["Node"]:
        if not self.is_dir:
            return
        max_list = [self.file_count()]
        node_list = [self]
        self.child_files(max_list, node_list)
        return node_list[max_list.index(max(max_list))]

    def get_sizes(self: "Node", sum_size: int):
        for child in self.children:
            if not child.is_dir:
                sum_size += child.size
            else:
                sum_size += child.get_sizes(0)
        return sum_size

    def get_size(self: "Node") -> int:
        sum_size = self.size
        return self.get_sizes(sum_size)

    # uloha 4
    def draw_children(self: "Node", depth: int, level_format: str) -> None:
        print(level_format, end="")
        print("-- " + self.name)
        size = len(self.children)
        depth += 4
        children = sorted(self.children, key=lambda c: c.name)
        for i in range(size):
            child = children[i]
            if i == size - 1:
                level_format += "    "
            else:
                level_format += "   |"
            child.draw_children(depth, level_format)
            level_format = level_format[:(depth - 4)]

    def draw_filesystem(self: "Node") -> None:
        depth = 0
        level_format = ""
        self.draw_children(depth, level_format)

    # uloha 5
    def kill_big_files(self: "Node", size: int, grave: "Node") -> None:
        for i in range(len(self.children)):
            if (not self.children[i].is_dir) \
                    and (self.children[i].size >= size):
                self.children[i] = grave
            elif self.children[i].is_dir:
                self.children[i].kill_big_files(size, grave)

    # uloha 6
    def let_children_owner(self: "Node", user: str) -> None:
        for x in range(len(self.children) - 1, -1, -1):
            if self.children[x].owner != user:
                del self.children[x]
        for child in self.children:
            if child.is_dir:
                child.let_children_owner(user)

    def let_by_owner(self: "Node", user: str) -> bool:
        if self.owner != user:
            self.children = []
            return True
        self.let_children_owner(user)
        return False

    def remove_empty_rest(self: "Node") -> None:
        for x in range(len(self.children) - 1, -1, -1):
            if self.children[x].is_dir:
                self.children[x].remove_empty_rest()
                if not self.children[x].children:
                    del self.children[x]

    def remove_empty_directories(self: "Node") -> bool:
        self.remove_empty_rest()
        if (not self.children) and (self.is_dir):
            return True
        return False


def find_node(nodes: List[Tuple[str, str, bool, int]],
              root_name: str) -> Optional[Tuple[str, str, bool, int]]:
    for node in nodes:
        if node[0] == root_name:
            return node
    return


def create_tree(nodes: List[Tuple[str, str, bool, int]],
                relations: List[Tuple[str, str]], parent_name: str,
                parent: "Node") -> None:
    for relation in relations:
        if relation[0] == parent_name:
            node_info = find_node(nodes, relation[1])
            node = Node(node_info[0], node_info[1], node_info[2], node_info[3],
                        parent, [])
            parent.children.append(node)
            create_tree(nodes, relations, node_info[0], node)


def build_tree(nodes: List[Tuple[str, str, bool, int]],
               relations: List[Tuple[str, str]]) -> Optional[Node]:
    if not nodes:
        return None
    root_name = nodes[0][0]
    parent_list: List[str] = []
    children_list: List[str] = []
    # create list of parents and children
    for name in relations:
        if name[0] not in parent_list:
            parent_list.append(name[0])
        if name[1] not in children_list:
            children_list.append(name[1])
    # finding name of root
    for nam in parent_list:
        if nam not in children_list:
            root_name = nam
            break
    # finding root node
    root = find_node(nodes, root_name)
    # building from root
    final_tree = Node(root[0], root[1], root[2], root[3], None, [])
    create_tree(nodes, relations, root_name, final_tree)
    return final_tree
