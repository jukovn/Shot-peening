# -*- coding: utf-8 -*-
from Node_class import Node
from Element_class import El_Brick8
from numpy import linspace,zeros,sign
from subprocess import check_call,Popen
from os import chdir, mkdir
import matplotlib.pyplot as plt


def Multi_output(dynain_path, POINTStress_path, output_points_path):

	CalcResults_output(dynain_path , dynain_path );
	SigPointData_print(POINTStress_path , dynain_path, output_points_path );



def CalcResults_output(res_dynain_path,res_output_path):

	Dynain_path = res_dynain_path + "\\dynain";

	# print Dynain_path;

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

	f1.close();

	f1 = open(Dynain_path,'r');
	str1 = f1.readline();

	while str1.find('*ELEMENT_SOLID') == -1:
		str1 = f1.readline();

	str1 = f1.readline();

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

	f1.close();

	f1 = open(Dynain_path,'r');
	str1 = f1.readline();

	while str1.find('*INITIAL_STRESS_SOLID') == -1:
		str1 = f1.readline();

	str1 = f1.readline();
	str1 = f1.readline();

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

		str1 = f1.readline();

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


	# forming ans_model.txt

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


def SigPointData_print(Ciam_stress_path,currcalc_path, Output_points_path):

	pathdata_path = Ciam_stress_path + '\\CurrPath.dat'
	
	f1 = open(pathdata_path,'w');
	f1.write(currcalc_path + "\n");
	f1.write(Output_points_path);
	f1.close();

	chdir(Ciam_stress_path);
	res_sp = check_call(['POINT_stress.exe']);


# def SigData_plot():

# 	Popen(['python' , 'Data_plot.py'] );


def XYData_det(x_ar,y_ar,x):

	n = x_ar.size;

	y = -1;
	i = 0;

	while y == -1 and i<(n-1):
		if (x<=x_ar[i+1]) and (x>=x_ar[i]):

			x1 = x_ar[i];
			x2 = x_ar[i+1];
			y1 = y_ar[i];
			y2 = y_ar[i+1];

			k = (y1 - y2)/(x1 - x2);
			b = (y2*x1 - y1*x2)/(x1 - x2);

			y = k*x + b;


		i = i + 1;

	if y == -1:

		if x<=x_ar[0]:
			y = 0;
		if x>=x_ar[-1]:
			y = y_ar[-1];

	return y;



def SigData_plot(calc_path,sigdata_path,pointsdata_path):


	points_data_path = pointsdata_path + "\\Output_points.dat";
	points_sig_data_path = sigdata_path + "\\sig_data_points.dat";


	f1 = open(points_data_path,'r');

	str1 = f1.readline();

	q = str1.find(" ");
	points_num = int(str1[:q]);
	str1 = str1[q+1:];

	q = str1.find(" ");
	num_xy_level = int(str1[:q]);
	str1 = str1[q+1:];

	q = str1.find(" ");
	str1 = str1[q+1:];

	num_z_level = int(str1);

	z_p = zeros((num_xy_level,num_xy_level,num_z_level));

	for i in range(points_num):
		str1 = f1.readline();

		q = str1.find(' ');
		str1 = str1[q+1:];

		q = str1.find(' ');
		str1 = str1[q+1:];

		z_p[i/(num_xy_level*num_z_level)][ (i%(num_xy_level*num_z_level))/num_z_level ][i%num_z_level] = float(str1);


	f1.close();



	f1 = open(points_sig_data_path,'r');

	sigxx_p = zeros((num_xy_level,num_xy_level,num_z_level));
	sigyy_p = zeros((num_xy_level,num_xy_level,num_z_level));
	sigzz_p = zeros((num_xy_level,num_xy_level,num_z_level));
	sigxy_p = zeros((num_xy_level,num_xy_level,num_z_level));
	sigxz_p = zeros((num_xy_level,num_xy_level,num_z_level));
	sigyz_p = zeros((num_xy_level,num_xy_level,num_z_level));

	eq_pl_str_p = zeros((num_xy_level,num_xy_level,num_z_level));

	for i in range(points_num):
		str1 = f1.readline();

		q = str1.find(' ');
		sigxx_p[i/(num_xy_level*num_z_level)][ (i%(num_xy_level*num_z_level))/num_z_level ][i%num_z_level] = float(str1[:q]);
		str1 = str1[q+1:];

		q = str1.find(' ');
		sigyy_p[i/(num_xy_level*num_z_level)][ (i%(num_xy_level*num_z_level))/num_z_level ][i%num_z_level] = float(str1[:q]);
		str1 = str1[q+1:];

		q = str1.find(' ');
		sigzz_p[i/(num_xy_level*num_z_level)][ (i%(num_xy_level*num_z_level))/num_z_level ][i%num_z_level] = float(str1[:q]);
		str1 = str1[q+1:];

		q = str1.find(' ');
		sigxy_p[i/(num_xy_level*num_z_level)][ (i%(num_xy_level*num_z_level))/num_z_level ][i%num_z_level] = float(str1[:q]);
		str1 = str1[q+1:];

		q = str1.find(' ');
		sigxz_p[i/(num_xy_level*num_z_level)][ (i%(num_xy_level*num_z_level))/num_z_level ][i%num_z_level] = float(str1[:q]);
		str1 = str1[q+1:];

		q = str1.find(' ');
		sigyz_p[i/(num_xy_level*num_z_level)][ (i%(num_xy_level*num_z_level))/num_z_level ][i%num_z_level] = float(str1[:q]);
		str1 = str1[q+1:];

		q = str1.find(' ');
		eq_pl_str_p[i/(num_xy_level*num_z_level)][ (i%(num_xy_level*num_z_level))/num_z_level ][i%num_z_level] = float(str1);

	f1.close();

	


	depth_ar = zeros((num_xy_level,num_xy_level,num_z_level));
	depth_shift_ar = zeros((num_xy_level,num_xy_level));


	for j in range(num_z_level):
		for i1 in range(num_xy_level):
			for i2 in range(num_xy_level):

				depth_ar[i1][i2][j] = 1e6*(z_p[0][0][0] - z_p[0][0][j]);


	for i1 in range(num_xy_level):
		for i2 in range(num_xy_level):

			j = 0;
			while sigyy_p[i1][i2][j] == 0:
				j = j + 1;

			depth_shift_ar[i1][i2] = int(j);



	gen_depth_ar = depth_ar[0][0];

	sigxx_average = zeros((num_z_level));
	sigyy_average = zeros((num_z_level));
	sigzz_average = zeros((num_z_level));
	sigxy_average = zeros((num_z_level));
	sigyz_average = zeros((num_z_level));
	sigxz_average = zeros((num_z_level));

	eq_pl_str_average = zeros((num_z_level));

	for i1 in range(num_z_level):
		for i2 in range(num_xy_level):
			for i3 in range(num_xy_level):

				sigxx_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigxx_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);
				sigyy_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigyy_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);
				sigzz_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigzz_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);
				sigxy_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigxy_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);
				sigyz_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigyz_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);
				sigxz_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigxz_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);

				eq_pl_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , eq_pl_str_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1])

				sigxx_average[i1] = sigxx_average[i1] + sigxx_temp;
				sigyy_average[i1] = sigyy_average[i1] + sigyy_temp;
				sigzz_average[i1] = sigzz_average[i1] + sigzz_temp;
				sigxy_average[i1] = sigxy_average[i1] + sigxy_temp;
				sigyz_average[i1] = sigyz_average[i1] + sigyz_temp;
				sigxz_average[i1] = sigxz_average[i1] + sigxz_temp;

				eq_pl_str_average[i1] = eq_pl_str_average[i1] + eq_pl_temp;



		sigxx_average[i1] = sigxx_average[i1]/num_xy_level/num_xy_level;
		sigyy_average[i1] = sigyy_average[i1]/num_xy_level/num_xy_level;
		sigzz_average[i1] = sigzz_average[i1]/num_xy_level/num_xy_level;
		sigxy_average[i1] = sigxy_average[i1]/num_xy_level/num_xy_level;
		sigyz_average[i1] = sigyz_average[i1]/num_xy_level/num_xy_level;
		sigxz_average[i1] = sigxz_average[i1]/num_xy_level/num_xy_level;

		eq_pl_str_average[i1] = eq_pl_str_average[i1]/num_xy_level/num_xy_level;




	# расчет значения дисперсии компонент тензора напряжения и эквивалентной пластической деформации по глубине эпюры среди точек площадки

	sigxx_var = zeros((num_z_level));
	sigyy_var = zeros((num_z_level));
	sigzz_var = zeros((num_z_level));
	sigxy_var = zeros((num_z_level));
	sigyz_var= zeros((num_z_level));
	sigxz_var = zeros((num_z_level));

	eq_pl_str_var = zeros((num_z_level));

	for i1 in range(num_z_level):
		for i2 in range(num_xy_level):
			for i3 in range(num_xy_level):

				sigxx_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigxx_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);
				sigyy_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigyy_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);
				sigzz_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigzz_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);
				sigxy_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigxy_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);
				sigyz_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigyz_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);
				sigxz_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , sigxz_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);

				eq_pl_temp = XYData_det(depth_ar[i2][i3][:-int(depth_shift_ar[i2][i3])] , eq_pl_str_p[i2][i3][int(depth_shift_ar[i2][i3]):] , gen_depth_ar[i1]);


				sigxx_var[i1] = sigxx_var[i1] + (sigxx_temp - sigxx_average[i1])**2;
				sigyy_var[i1] = sigyy_var[i1] + (sigyy_temp - sigyy_average[i1])**2;
				sigzz_var[i1] = sigzz_var[i1] + (sigzz_temp - sigzz_average[i1])**2;
				sigxy_var[i1] = sigxy_var[i1] + (sigxy_temp - sigxy_average[i1])**2;
				sigyz_var[i1] = sigyz_var[i1] + (sigyz_temp - sigyz_average[i1])**2;
				sigxz_var[i1] = sigxz_var[i1] + (sigxz_temp - sigxz_average[i1])**2;

				eq_pl_str_var[i1] = eq_pl_str_var[i1] + (eq_pl_temp - eq_pl_str_average[i1])**2;



		# sigxx_var[i1] = sigxx_var[i1]/sigxx_average[i1];
		# sigyy_var[i1] = sigyy_var[i1]/sigyy_average[i1];
		# sigzz_var[i1] = sigzz_var[i1]/sigzz_average[i1];
		# sigxy_var[i1] = sigxy_var[i1]/sigxy_average[i1];
		# sigyz_var[i1] = sigyz_var[i1]/sigyz_average[i1];
		# sigxz_var[i1] = sigxz_var[i1]/sigxz_average[i1];

		# eq_pl_str_var[i1] = eq_pl_str_var[i1]/eq_pl_str_average[i1];

		sigxx_var[i1] = sigxx_var[i1]/num_xy_level/num_xy_level;
		sigyy_var[i1] = sigyy_var[i1]/num_xy_level/num_xy_level;
		sigzz_var[i1] = sigzz_var[i1]/num_xy_level/num_xy_level;
		sigxy_var[i1] = sigxy_var[i1]/num_xy_level/num_xy_level;
		sigyz_var[i1] = sigyz_var[i1]/num_xy_level/num_xy_level;
		sigxz_var[i1] = sigxz_var[i1]/num_xy_level/num_xy_level;

		eq_pl_str_var[i1] = eq_pl_str_var[i1]/num_xy_level/num_xy_level;


	

	# for i1 in range(num_z_level):
	# 	for i2 in range(num_xy_level):
	# 		for i3 in range(num_xy_level):

	# 			sigxx_average[i1] = sigxx_average[i1] + XYData_det(depth_ar[i2][i3][:-depth_shift_ar[i2][i3]] , sigxx_p[i2][i3][depth_shift_ar[i2][i3]:] , gen_depth_ar[i1]);


	# вывод файла с осредненными эпюрами компонент НДС для загрузки в ANSYS

	f1 = open(calc_path + "\\ANSYS_sig.txt",'w');

	f1.write(str(num_z_level) + '\n');

	for i in range(num_z_level):
		str_tmp = "{:22.15E}  {:22.15E}  {:22.15E}  {:22.15E}  {:22.15E}  {:22.15E}  {:22.15E}  {:22.15E}".format(gen_depth_ar[i]*1e-3,sigxx_average[i]/1e6,sigyy_average[i]/1e6,sigzz_average[i]/1e6,sigxy_average[i]/1e6,sigxz_average[i]/1e6,sigyz_average[i]/1e6,eq_pl_str_average[i]);
		f1.write(str_tmp + "\n");

	f1.close();


	# построение эпюр

	# построение эпюр в крайних угловых и центральной точке выделенной площадки на обрабатываемой поверхности

	plt.figure(1);

	

	
	plt.subplot(3,3,1);
	plt.plot(depth_ar[0][0][:-int(depth_shift_ar[0][0])],sigyy_p[0][0][int(depth_shift_ar[0][0]):]);
	plt.xlabel('h, mcm');
	plt.ylabel('Sigyy, Pa')
	plt.grid();
	plt.title('1-st corner point');


	plt.subplot(3,3,3);
	plt.plot(depth_ar[-1][0][:-int(depth_shift_ar[-1][0])],sigyy_p[-1][0][int(depth_shift_ar[-1][0]):]);
	plt.xlabel('h, mcm');
	plt.ylabel('Sigyy, Pa')
	plt.grid();
	plt.title('2-nd corner point');

	plt.subplot(3,3,5);
	plt.plot(depth_ar[num_xy_level/2][num_xy_level/2][:-int(depth_shift_ar[num_xy_level/2][num_xy_level/2])],sigyy_p[num_xy_level/2][num_xy_level/2][int(depth_shift_ar[num_xy_level/2][num_xy_level/2]):]);
	plt.xlabel('h, mcm');
	plt.ylabel('Sigyy, Pa')
	plt.grid();
	plt.title('center point');

	plt.subplot(3,3,7);
	plt.plot(depth_ar[0][-1][:-int(depth_shift_ar[0][-1])],sigyy_p[0][-1][int(depth_shift_ar[0][-1]):]);
	plt.grid();
	plt.xlabel('h, mcm');
	plt.ylabel('Sigyy, Pa');
	plt.title('3-rd corner point');

	plt.subplot(3,3,9);
	plt.plot(depth_ar[-1][-1][:-int(depth_shift_ar[-1][-1])],sigyy_p[-1][-1][int(depth_shift_ar[-1][-1]):]);
	plt.xlabel('h, mcm');
	plt.ylabel('Sigyy, Pa')
	plt.grid();
	plt.title('4-th corner point');

	# построение осредненных по площади эпюр

	plt.figure(2);
	plt.plot(gen_depth_ar,sigxx_average);
	plt.xlabel('h, mcm');
	plt.ylabel('Sigxx, Pa')
	plt.title('SigXX averaged');
	plt.grid();


	plt.figure(3);
	plt.plot(gen_depth_ar,sigyy_average);
	plt.xlabel('h, mcm');
	plt.ylabel('Sigyy, Pa')
	plt.title('SigYY averaged');
	plt.grid();

	plt.figure(4);
	plt.plot(gen_depth_ar,sigzz_average);
	plt.xlabel('h, mcm');
	plt.ylabel('Sigzz, Pa')
	plt.title('SigZZ averaged');
	plt.grid();

	plt.figure(5);
	plt.plot(gen_depth_ar,sigxx_var);
	plt.xlabel('h, mcm');
	plt.ylabel('Sigxx, Pa')
	plt.title('SigXX variation');
	plt.grid();

	plt.figure(6);
	plt.plot(gen_depth_ar,sigyy_var);
	plt.xlabel('h, mcm');
	plt.ylabel('Sigyy, Pa')
	plt.title('SigYY variation');
	plt.grid();

	plt.figure(7);
	plt.plot(gen_depth_ar,eq_pl_str_var);
	plt.xlabel('h, mcm');
	plt.ylabel('Eq_pl Pa')
	plt.title('Eq_pl variation');
	plt.grid();

	print "Sigxx:";
	print "max = ",max(abs(sigxx_average))/1e6, "MPa";
	print "max variation = ", max(sigxx_var);
	for i in range(num_z_level):
		if abs(sigxx_average[i]) == max(abs(sigxx_average)):
			k=i;
	print "depth max = ",gen_depth_ar[k];
	k=0;
	i=0;
	while k==0:

		if sign(sigxx_average[i]) != sign(sigxx_average[i+1]):
			k=i;

		i = i + 1
	print "sig = 0: h = ", gen_depth_ar[k] + abs(sigxx_average[k])*(gen_depth_ar[k+1] - gen_depth_ar[k])/( abs(sigxx_average[k]) + abs(sigxx_average[k+1]) );
	print ;#"\n\n";

	print "Sigyy:";
	print "max = ",max(abs(sigyy_average))/1e6, "MPa";
	print "max variation = ", max(sigyy_var);
	for i in range(num_z_level):
		if abs(sigyy_average[i]) == max(abs(sigyy_average)):
			k=i;
	print "depth max = ",gen_depth_ar[k];
	k=0;
	i=0;
	while k==0:

		if sign(sigyy_average[i]) != sign(sigyy_average[i+1]):
			k=i;

		i = i + 1
	print "sig = 0: h = ", gen_depth_ar[k] + abs(sigyy_average[k])*(gen_depth_ar[k+1] - gen_depth_ar[k])/( abs(sigyy_average[k]) + abs(sigyy_average[k+1]) );
	print ;#"\n\n";
	
	print "Sigzz:";
	print "max = ",max(abs(sigzz_average))/1e6, "MPa";
	for i in range(num_z_level):
		if abs(sigzz_average[i]) == max(abs(sigzz_average)):
			k=i;
	print "depth max = ",gen_depth_ar[k];
	# k=0;
	# i=0;
	# while k==0:

	# 	if sign(sigzz_average[i]) != sign(sigzz_average[i+1]):
	# 		k=i;

	# 	i = i + 1
	# print "sig = 0: h = ", gen_depth_ar[k] + abs(sigzz_average[k])*(gen_depth_ar[k+1] - gen_depth_ar[k])/( abs(sigzz_average[k]) + abs(sigzz_average[k+1]) );
	print ;#"\n\n";


	print "max averaged pl str = ", max(eq_pl_str_average);
	print "max pl str = ", max(eq_pl_str_p[num_xy_level/2][num_xy_level/2][int(depth_shift_ar[num_xy_level/2][num_xy_level/2]):]);
	print "max pl str variance = ", max(eq_pl_str_var);




	plt.show();



