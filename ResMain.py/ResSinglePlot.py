# -*- coding: utf-8 -*-

#
# программа для построения эпюр для единичных результатов расчета
#

from PostProc import CalcResults_output,SigPointData_print,SigData_plot


if __name__ == "__main__":

	dynain_path = 'E:\\CIAM_stress\\Prog_v.1.1\\V60_R0.08_0.1\\Res\\Shot50'; # директория файла dynain, содержащая файл sig_data_points.dat
	output_points_path = "E:\\CIAM_stress\\Prog_v.1.1"; # директория файла output_points.dat


	SigData_plot(dynain_path, dynain_path, output_points_path);