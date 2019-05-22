# 链式线性表思路：
# 1.　节点如何表示
#   自定义对象：对象及数据，对象属性即数据元素
#   数据元素：包含有用数据和记录下一个对象地址的数据
# 2.　如何建立关联
# 3.　实现什么样的链表操作？
"""
单链表学习程序
重点程序
"""


# 1.创建节点类
class Node():
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


# 2.链表的操作
class LinkList:
    def __init__(self):  # 头节点
        self.head = None

    def init_list(self, l):
        self.head = Node(None)  # 链表的开头
        p = self.head  #  p可移动变量

        for i in l:
            p.next = Node(i)
            p = p.next

    def show(self):
        p = self.head.next
        while p:
            print (p.val)
            p = p.next
        print()

# 3.创建链表对象
if __name__ == "__main__":
    link = LinkList()
    # 初始数据
    L = [1, 2, 3, 45, 6]
    link.init_list(L)  # 将初始数据插入链表
    link.show()

