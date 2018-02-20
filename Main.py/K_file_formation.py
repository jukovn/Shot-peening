# -*- coding: utf-8 -*-
from Target_class import Target
from Shot_solid_class import Shot
from Control_class import Control

def FullMacFile_form(MacFile_path,Data_path,total_shots):
	
	#path = "E:\\Nikita\\CIAM\\2017\\LS_DYNA\\Projects\\Python_macros\\Python_prog\\";
	File_name = "Mac.k";
	Full_path = MacFile_path + File_name;


	f1 = open(Full_path,'w');
	f1.write("*KEYWORD\n");
	f1.close();

	target = Target();
	# target.DataInit();
	target.FirstDataInit(MacFile_path);
	target.Full_print(Full_path);

	# print target.elements_num,target.nodes_num;

	shots = [];

	curr_node_num = target.nodes_num;
	curr_elem_num = target.elements_num;
	t = 0;
	dt = 0.5e-6;

	for i in range(total_shots):
		shot_tmp = Shot(target.a , target.c , target.border , i , t , t + dt , Data_path);
		shot_tmp.DataInit(MacFile_path,curr_node_num,curr_elem_num);
		shot_tmp.Full_print(Full_path);

		curr_node_num = curr_node_num + shot_tmp.nodes_num;
		curr_elem_num = curr_elem_num + shot_tmp.elements_num;
		t = t + dt;


	control = Control(dt * total_shots, dt);
	control.Full_print(Full_path);


	f1 = open(Full_path,'a');
	f1.write("*END");
	f1.close();

	del target;

def OutputPointsPrint(dir_path):

	target = Target();
	target.FirstDataInit(dir_path);
