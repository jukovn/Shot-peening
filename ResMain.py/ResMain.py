# -*- coding: utf-8 -*-
from PostProc import CalcResults_output,SigPointData_print,SigData_plot


if __name__ == "__main__":

	dynain_path = 'E:\\CIAM_stress\\Prog_v.1.1\\V60_R0.08_0.1\\Res\\Shot50'; # директория файла dynain
	POINTStress_path = "C:\\Nikita\\NII_APP\\CIAM\\Program\\Shot-peening\\ResMain.py";# директория программы Point_stress.exe
	output_points_path = "E:\\CIAM_stress\\Prog_v.1.1"; # директория файла output_points.dat


	CalcResults_output(dynain_path , dynain_path );
	SigPointData_print(POINTStress_path , dynain_path, output_points_path );
	SigData_plot(dynain_path, dynain_path, output_points_path);