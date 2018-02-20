from Node_class import Node
from Element_class import El_Brick8
from numpy import linspace,zeros
from subprocess import check_call,Popen
from os import chdir, mkdir


def CalcResults_output(res_dynain_path,res_output_path):

	# Dynain_path = "E:\\Nikita\\CIAM\\2017\\LS_DYNA\\Projects\\Python_macros\\Python_prog\\";
	Dynain_path = res_dynain_path + "\\dynain";

	print Dynain_path;

	f1 = open(Dynain_path,'r');
	str1 = f1.readline();

	while str1.find('*NODE') == -1:
		str1 = f1.readline();
	str1 = f1.readline();

	node_num = 0;
	nodes = [];

	while str1.find('*') == -1:
		
		Node_temp = Node();

		Node_temp.num = int(str1[:8]);
		Node_temp.x = float(str1[8:24]);
		Node_temp.y = float(str1[24:40]);
		Node_temp.z = float(str1[40:56]);

		nodes.append(Node_temp);

		str1 = f1.readline();
		node_num = node_num + 1;

		# print str1;

	f1.close();

	f1 = open(Dynain_path,'r');
	str1 = f1.readline();

	while str1.find('*ELEMENT_SOLID') == -1:
		str1 = f1.readline();

	str1 = f1.readline();

	# print str1;

	el_num = 0;
	elements = [];

	while str1.find('*') == -1:

		El_temp = El_Brick8();

		El_temp.num = int(str1[:8]);

		for i in range(8):

			node_tmp_num = int(str1[(16 + 8*i) : (24 + 8*i)])

			El_temp.Add_Node(nodes[node_tmp_num - 1]);

		elements.append(El_temp);

		str1 = f1.readline();
		el_num = el_num + 1;

		# print str1;

	f1.close();

	f1 = open(Dynain_path,'r');
	str1 = f1.readline();

	while str1.find('*INITIAL_STRESS_SOLID') == -1:
		str1 = f1.readline();

	str1 = f1.readline();
	str1 = f1.readline();

	# print str1;


	sigxx_el = [];
	sigyy_el = [];
	sigzz_el = [];
	sigxy_el = [];
	sigxz_el = [];
	sigyz_el = [];

	eq_pl_str_el = [];

	while str1.find('*') == -1:

		str1 = f1.readline();

		sigxx_el.append(float(str1[:16]));
		sigyy_el.append(float(str1[16:32]));
		sigzz_el.append(float(str1[32:48]));
		sigxy_el.append(float(str1[48:64]));
		sigyz_el.append(float(str1[64:80]));

		str1 = f1.readline();
		sigxz_el.append(float(str1[:16]));
		eq_pl_str_el.append(float(str1[16:32]));

		# for i in range(7):
		# 	str1 = f1.readline();

		# 	sigxx_el[-1] = sigxx_el[-1] + float(str1[:16]);
		# 	sigyy_el[-1] = sigyy_el[-1] + float(str1[16:32]);
		# 	sigzz_el[-1] = sigzz_el[-1] + float(str1[32:48]);
		# 	sigxy_el[-1] = sigxy_el[-1] + float(str1[48:64]);
		# 	sigyz_el[-1] = sigyz_el[-1] + float(str1[64:80]);

		# 	str1 = f1.readline();

		# 	sigxz_el[-1] = sigxz_el[-1] + float(str1[:16]);
		# 	eq_pl_str_el[-1] = eq_pl_str_el[-1] + float(str1[16:32]);


		# sigxx_el[-1] = sigxx_el[-1]/8.0;
		# sigyy_el[-1] = sigyy_el[-1]/8.0;
		# sigzz_el[-1] = sigzz_el[-1]/8.0;
		# sigxy_el[-1] = sigxy_el[-1]/8.0;
		# sigxz_el[-1] = sigxz_el[-1]/8.0;
		# sigyz_el[-1] = sigyz_el[-1]/8.0;
		# eq_pl_str_el[-1] = eq_pl_str_el[-1]/8.0;

		str1 = f1.readline();

		# print str1;


	# print sigxx_el[0],sigyy_el[0],sigzz_el[0],sigxy_el[0],sigxz_el[0],sigyz_el[0];
	# print sigxx_el[-1],sigyy_el[-1],sigzz_el[-1],sigxy_el[-1],sigxz_el[-1],sigyz_el[-1];


	f1.close();

	sigxx = [];
	sigyy = [];
	sigzz = [];
	sigxy = [];
	sigxz = [];
	sigyz = [];

	eq_pl_str = [];

	for i in range(node_num):

		sigxx.append(0.0);
		sigyy.append(0.0);
		sigzz.append(0.0);
		sigxy.append(0.0);
		sigxz.append(0.0);
		sigyz.append(0.0);

		eq_pl_str.append(0.0);

	for i in range(el_num):

		for j in range(8):

			sigxx[elements[i].nodes[j].num - 1] = sigxx[elements[i].nodes[j].num - 1] + 1.0/8.0*sigxx_el[i];
			sigyy[elements[i].nodes[j].num - 1] = sigyy[elements[i].nodes[j].num - 1] + 1.0/8.0*sigyy_el[i];
			sigzz[elements[i].nodes[j].num - 1] = sigzz[elements[i].nodes[j].num - 1] + 1.0/8.0*sigzz_el[i];
			sigxy[elements[i].nodes[j].num - 1] = sigxy[elements[i].nodes[j].num - 1] + 1.0/8.0*sigxy_el[i];
			sigxz[elements[i].nodes[j].num - 1] = sigxz[elements[i].nodes[j].num - 1] + 1.0/8.0*sigxz_el[i];
			sigyz[elements[i].nodes[j].num - 1] = sigyz[elements[i].nodes[j].num - 1] + 1.0/8.0*sigyz_el[i];

			eq_pl_str[elements[i].nodes[j].num - 1] = eq_pl_str[elements[i].nodes[j].num - 1] + 1.0/8.0*eq_pl_str_el[i];






	# print nodes[0].num,nodes[0].x,nodes[0].y,nodes[0].z
	# print nodes[28610].num,nodes[28610].x,nodes[28610].y,nodes[28610].z;

	# print elements[0].num,elements[0].node1.num,elements[0].node2.num,elements[0].node3.num,elements[0].node4.num,elements[0].node5.num,elements[0].node6.num,elements[0].node7.num,elements[0].node8.num
	# print elements[24999].num,elements[24999].node1.num,elements[24999].node2.num,elements[24999].node3.num,elements[24999].node4.num,elements[24999].node5.num,elements[24999].node6.num,elements[24999].node7.num,elements[24999].node8.num

	### forming ans_model.txt

	ans_model_path = res_output_path;
	ans_model_path = ans_model_path + "\\ans_model.txt";


	f1 = open(ans_model_path,'w');

	f1.write('3\n');
	f1.write(str(node_num) + '\n');
	f1.write(str(el_num) + '\n');
	f1.write('1.000000e+000\n');
	f1.write('1.000000e+000\n');
	f1.write('1\n');
	f1.write('1\n');
	f1.write('2.660000e+003\n');
	f1.write('7.200000e+010\n');
	f1.write('3.300000e-001\n');
	f1.write('1\n');
	f1.write('45\n');
	f1.write('0\n');
	f1.write('1\n');
	f1.write('2\n');

	for i in range(node_num):

		f1.write(str(nodes[i].num) + '  ' + str(nodes[i].x) + '  ' + str(nodes[i].y) + '  ' + str(nodes[i].z) + '\n');

	for i in range(el_num):

		f1.write('1 1 0 0 0 0 0 0 8 0 ' + str(elements[i].num) + ' ' + str(elements[i].node1.num) + ' ' + str(elements[i].node2.num) + ' ' + str(elements[i].node3.num) + ' ' + str(elements[i].node4.num) + ' ' + str(elements[i].node5.num) + ' ' + str(elements[i].node6.num) + ' ' + str(elements[i].node7.num) + ' ' + str(elements[i].node8.num) + '\n')

	f1.write('0\n');
	f1.close();

	# sig file forming

	sig_data_path = res_output_path;
	sig_data_path = sig_data_path + "\\sig_data.dat";

	f1 = open(sig_data_path,'w');

	for i in range(node_num):

		f1.write(str(nodes[i].num) + ' ' + str(sigxx[i]) + ' ' + str(sigyy[i]) + ' ' + str(sigzz[i]) + ' ' + str(sigxy[i]) + ' ' + str(sigxz[i]) + ' ' + str(sigyz[i]) + ' ' + str(eq_pl_str[i]) + '\n' ); 

	f1.close();


def SigPointData_print(Ciam_stress_path,currcalc_path):

	pathdata_path = Ciam_stress_path + '\\CurrPath.dat'
	
	f1 = open(pathdata_path,'w');
	f1.write(currcalc_path);
	f1.close();

	chdir(Ciam_stress_path);
	res_sp = check_call(['POINT_stress.exe']);


def SigData_plot():

	Popen(['python' , 'Data_plot.py'] );

def SigDataRelief_plot():

	Popen(['python' , 'Data_relief_plot.py'] );











	# sig_points_path = "E:\\Nikita\\CIAM\\2017\\LS_DYNA\\Projects\\Python_macros\\Python_prog\\";
	# sig_points_path = sig_points_path + "sig_data_points.dat";

	# sigxx_p = [];
	# sigyy_p = [];
	# sigzz_p = [];
	# sigxy_p = [];
	# sigxz_p = [];
	# sigyz_p = [];


	# f1 = open(sig_points_path,'r');

	# for i in range(len(x_p)):

	# 	str1 = f1.readline();

	# 	q = str1.find(' ');
	# 	sigxx_p.append(float(str1[:q]));
	# 	str1 = str1[q+1:];

	# 	q = str1.find(' ');
	# 	sigyy_p.append(float(str1[:q]));
	# 	str1 = str1[q+1:];

	# 	q = str1.find(' ');
	# 	sigzz_p.append(float(str1[:q]));
	# 	str1 = str1[q+1:];

	# 	q = str1.find(' ');
	# 	sigxy_p.append(float(str1[:q]));
	# 	str1 = str1[q+1:];

	# 	q = str1.find(' ');
	# 	sigxz_p.append(float(str1[:q]));
	# 	str1 = str1[q+1:];

	# 	q = str1.find(' ');
	# 	sigyz_p.append(float(str1[:q]));
	# 	str1 = str1[q+1:];

	# f1.close();

	# plt.figure();
	# plt.plot(-z_p,sigzz_p);

	# plt.show();

