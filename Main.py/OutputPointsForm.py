# -*- coding: utf-8 -*-
from subprocess import check_call
from os import chdir, mkdir, path
from K_file_formation import OutputPointsPrint;

if __name__ == "__main__":

	OutputPoints_path= 'C:\\Temp\\Calc_temp\\Res_without_relief\\Res_with_relief\\'; # директория расположения файла с КЭ-моделью шарика единичного радиуса

	if path.isdir(OutputPoints_path)!=True:
		mkdir(OutputPoints_path);
	OutputPointsPrint(OutputPoints_path);