# -*- coding: utf-8 -*-
from subprocess import check_call
from os import chdir, mkdir, path
from K_file_formation import FullMacFile_form;

if __name__ == "__main__":

	Data_path = 'C:\\Nikita\\NII_APP\\CIAM\\2018_article\\Program\\Main.py\\Data'; # директория расположения файла с КЭ-моделью шарика единичного радиуса
	Calc_path = 'C:\\Nikita\\NII_APP\\CIAM\\2018_article\\Program\\Main.py\\Temp_calc'; # директория расчета
	lsdyna_path = 'C:\\Program Files\\ANSYS Inc\\v170\\ansys\\bin\\winx64\\lsdyna.exe'; # директория расположения LSDYNA.exe

	NCPU = 8; # количество используемых ядер
	total_shots = 400; # общее количество шариков

	if path.isdir(Calc_path)!=True:
		mkdir(Calc_path);
	FullMacFile_form(Calc_path + '\\', Data_path + '\\',total_shots);
	chdir(Calc_path);

	# OutFile_path = Calc_path + '\\Out.dat';
	# f_out = open(OutFile_path,'w');
	# res_sp = check_call([lsdyna_path, 'pr=aa_r_dy' , 'memory=3000000000' , 'i=' + Calc_path + '\\Mac.k', 'NCPU=' + str(NCPU), 'PARA=1', '-DP' ], stdout = f_out);
	# f_out.close();


