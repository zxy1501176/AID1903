class data_struct:
    def __init__(self,value=None,next=None):
        self.value = value
        self.next = next

class linklist:
    def __init__(self):
        self.head =None

    def list_link(self,l):
        self.head = data_struct(None)
        p = self.head

        for i in l:
            p.next= data_struct(i)
            p =p.next


    def show(self):
        p = self.head.next
        while p:
            print(p.value,end= ' ')
            p = p.next
        print()

    def find_tail(self):
        p = self.head.next
        while p.next :
            p = p.next
        return  p

    def insert_tail(self,tail):
        p = self.find_tail()
        for i in tail:
            p.next= data_struct(i)
            p = p.next


node_header = linklist()
list_test = [1,2,3,4,5]
node_header.list_link(list_test)
node_header.show()

list_tail = [8,9,10]
node_header.insert_tail(list_tail)
node_header.show()
