from Node_class import Node

class El_Brick8(Node):
    
    node1=Node();
    node2=Node();
    node3=Node();
    node4=Node();
    node5=Node();
    node6=Node();
    node7=Node();
    node8=Node();
    
    nodes = [node1,node2,node3,node4,node5,node6,node7,node8]
    
    num = 0;
    nodes_num = 8;
    curr_node_num = 0;

    def __init__(self):
        
        self.node1=Node();
        self.node2=Node();
        self.node3=Node();
        self.node4=Node();
        self.node5=Node();
        self.node6=Node();
        self.node7=Node();
        self.node8=Node();

        self.nodes = [self.node1,self.node2,self.node3,self.node4,self.node5,self.node6,self.node7,self.node8]

        self.num = 0;
        self.nodes_num = 8;
        self.curr_node_num = 0;

    
    def Add_Node(self,node_temp):
        if self.curr_node_num < self.nodes_num:
            self.nodes[self.curr_node_num].num = node_temp.num;
            self.nodes[self.curr_node_num].x = node_temp.x;
            self.nodes[self.curr_node_num].y = node_temp.y;
            self.nodes[self.curr_node_num].z = node_temp.z;

            self.curr_node_num = self.curr_node_num + 1;


    # self.nodes.append(node_temp);

class El_Shell4(Node):
    
    node1=Node();
    node2=Node();
    node3=Node();
    node4=Node();

    nodes = [node1,node2,node3,node4]
    
    num = 0;
    nodes_num = 4;
    curr_node_num = 0;

    def __init__(self):
        self.node1=Node();
        self.node2=Node();
        self.node3=Node();
        self.node4=Node();

        self.nodes = [self.node1,self.node2,self.node3,self.node4]

        self.num = 0;
        self.nodes_num = 4;
        self.curr_node_num = 0;

    
    def Add_Node(self,node_temp):
        self.nodes[self.curr_node_num].num = node_temp.num;
        self.nodes[self.curr_node_num].x = node_temp.x;
        self.nodes[self.curr_node_num].y = node_temp.y;
        self.nodes[self.curr_node_num].z = node_temp.z;

        self.curr_node_num = self.curr_node_num + 1;