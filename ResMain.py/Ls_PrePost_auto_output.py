# -*- coding: utf-8 -*-
from subprocess import check_call
from os import chdir, mkdir, path
from PostProc import Multi_output

if __name__ == "__main__":

	# 
	# блок исходных данных
	# 

	# исходные директории

	Res_path = "E:\CIAM_stress\Prog_v.1.1\V60_R0.08_0.1"; # директория, в которой будух сохранены файлы dynain (путь задавать обязательно с одинарным '\')
	d3plot_path = "E:\CIAM_stress\Prog_v.1.1\V60_R0.08_0.1"; # путь к результатам расчета (к файлу d3plot) (путь задавать обязательно с одинарным '\')
	
	LS_PrePost_path = "C:\\Program Files\\LSTC\\LS-PrePost 4.5"; # путь к программе LS PrePost (путь задавать обязательно с двойным '\\')
	LS_PrePost_name = "lsprepost4.5_x64.exe"; # имя приложения LS PrePost из директории LS_PrePost_path
	LS_PrePost_macro_name = "Prog.dat"; # имя создаваемого макроса для LS PrePost (на всякий случаЙ, менять не обязательно!)

	Mac_add_path = "C:\\Nikita\\NII_APP\\CIAM\\Program\\Shot-peening\\ResMain.py\\Mac_add"; # путь к файлу Mac_add

	LS_Dyna_path = "C:\\LSDYNA\\program"; # путь к директории программы LS-Dyna
	LS_Dyna_name = "ls-dyna_smp_d_R700_winx64_ifort101.exe"; # имя программы в данной директории
	NCPU = 4; # количество CPU, используемых при расчете релаксации напряжений

	output_points_path = "E:\\CIAM_stress\\Prog_v.1.1"; # дирекктория файла output_points.dat
	POINTStress_path = "C:\\Nikita\\NII_APP\\CIAM\\Program\\Shot-peening\\ResMain.py"; # директория программы POINT_stress.exe
	
	# параметры проведенного расчета

	total_shots_num = 400; # общее количество шариков
	shots_interval = 50; # шаг вывода файлов dynain
	n_output = 0.5; # параметр из Control_class.py



	# 
	#  пересчет внутренних величин
	# 

	n_states = int(total_shots_num/shots_interval);# количество записываемых состояний
	d_shot_num = int(shots_interval);# количество шариков на один шаг записи файлов



	# 
	# создание системы директорий и макроса для LS PrePost
	# 

	Res_path_base = Res_path + "\Res";

	if path.isdir(Res_path_base)!=True:
		mkdir(Res_path_base);

	macro_path = Res_path_base + '\\' + LS_PrePost_macro_name;

	f_mac = open(macro_path, 'w');
 
	strtmp = "open d3plot " + d3plot_path + '\d3plot\n';
	f_mac.write(strtmp);
	strtmp = "ac\n";
	f_mac.write(strtmp);
	strtmp = "postmodel off\n+M 1\n";
	f_mac.write(strtmp);


	for i in range(n_states):

		curr_state_num = (i+1);

		Res_path_curr = Res_path_base + "\Shot" + str(curr_state_num*d_shot_num);
		if path.isdir(Res_path_curr)!=True:
			mkdir(Res_path_curr);

		strtmp = "output " + Res_path_curr + "\dynain_old " + str(int(curr_state_num*d_shot_num*n_output)) + " 4 0 1 0 0 0\n";
		f_mac.write(strtmp)

	f_mac.close();



	# 
	# запуск макроса в LS PrePost в batch-режиме
	# 

	# chdir(LS_PrePost_path);
	# res_sp = check_call([LS_PrePost_name, 'c=' + macro_path , '-nographics' ] );


	#
	# блок подготовки выведенных dynain-файлов для расчета релаксации напряжений
	#

	

	# for i in range(n_states):

	# 	curr_state_num = (i+1);
	# 	Res_path_curr = Res_path_base + "\Shot" + str(curr_state_num*d_shot_num);

	# 	f1 = open(Mac_add_path,'r');
	# 	f2 = open(Res_path_curr + "\\dynain_old",'r');
	# 	f3 = open(Res_path_curr + "\\Relief_mac.k","w");


	# 	strtmp = f2.readline();

	# 	while strtmp.find("*END") == -1:
	# 		f3.write(strtmp);
	# 		strtmp = f2.readline();

	# 	for strtmp in f1:
	# 		f3.write(strtmp);

	# 	f3.write("\n*END\n");


	# 	f3.close();
	# 	f2.close();
	# 	f1.close();


	#
	# блок расчета релаксации в LS-Dyna
	#


	# for i in range(n_states):

	# 	curr_state_num = (i+1);
	# 	Res_path_curr = Res_path_base + "\Shot" + str(curr_state_num*d_shot_num);


	# 	f_out = open(Res_path_curr + "\\Out.dat", 'w');
	# 	chdir(Res_path_curr);
	# 	res_sp = check_call([LS_Dyna_path + "\\" + LS_Dyna_name, 'pr=aa_r_dy' , 'memory=600M' , 'i=' + Res_path_curr + '\\Relief_mac.k', 'NCPU=' + str(NCPU), 'PARA=1'], stdout = f_out);
	# 	f_out.close();


	#
	# блок повторного вывода файлов dynain после релаксации
	#

	for i in range(n_states):

		curr_state_num = (i+1);
		Res_path_curr = Res_path_base + "\Shot" + str(curr_state_num*d_shot_num);	
		macro_path = Res_path_curr + '\\' + LS_PrePost_macro_name;

		f_mac = open(macro_path, 'w');
 
		strtmp = "open d3plot " + Res_path_curr + '\d3plot\n';
		f_mac.write(strtmp);
		strtmp = "ac\n";
		f_mac.write(strtmp);

		strtmp = "output " + Res_path_curr + "\dynain " + "8" + " 4 0 1 0 0 0\n";
		f_mac.write(strtmp)
		

		f_mac.close();

		chdir(LS_PrePost_path);
		res_sp = check_call([LS_PrePost_name, 'c=' + macro_path , '-nographics' ] );


	#
	# вывод промежуточных файлов результатов
	#

	for i in range(n_states):

		curr_state_num = (i+1);
		Res_path_curr = Res_path_base + "\Shot" + str(curr_state_num*d_shot_num);

		dynain_path = Res_path_curr;

		Multi_output(dynain_path, POINTStress_path, output_points_path)

