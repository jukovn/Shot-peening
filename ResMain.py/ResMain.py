# -*- coding: utf-8 -*-
from PostProc import CalcResults_output,SigPointData_print,SigData_plot


if __name__ == "__main__":

	Calc_path = 'G:\\CIAM_stress\\Res(el_type_1)\\Dynain_files\\Shot_500'; # директория файла dynain
	POINTStress_path = Calc_path;# 'C:\\Temp\\Calc_temp\\Res_without_relief\\Res_with_relief\\Shot250'; # директория программы Point_stress.exe

	# Файлы dynain, output_points.txt и программу point_stress.exe следует располагать в одной директории.
	# В результате работы программы в той же директории будет создан файл ANSYS_sig.txt, содержащий осредненные эпюры компонент НДС.
	# Файл впоследствие используется для запуска макроса на ANSYS (reading_applying_stress_by_el.txt).

	CalcResults_output(Calc_path , Calc_path );
	SigPointData_print(POINTStress_path , Calc_path);
	SigData_plot(Calc_path,Calc_path,Calc_path);