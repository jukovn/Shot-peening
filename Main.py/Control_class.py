class Control():
	#comment added!

	Time = 0.0;#4.0e-6;
	dt = 0;#2e-20;

	restart_dt = 0.0;

	n_output = 0.5;

	red_par = 0.2;

	def __init__(self,full_time,dt):

		self.Time = full_time;
		self.dt = dt;

		self.restart_dt = dt/1.2e-10*30;

	def Termination_print(self,path):

		f = open(path,'a');
		f.write("*CONTROL_TERMINATION\n");

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}\n".format(self.Time,0,0.0,0.0,1e8);
		f.write(str_tmp);

		f.close();

	def Timestep_print(self,path):

		red_par = self.red_par; # 0.9

		f = open(path,'a');
		f.write("*CONTROL_TIMESTEP\n");

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(self.dt,red_par,0,0.0,0.0,0,0,0);
		f.write(str_tmp);

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>30}\n".format(0.0,0,0,0.0);
		f.write(str_tmp);

		f.close();


	def Implicit_print(self,path):

		imflag = 1;

		f = open(path,'a');
		f.write("*CONTROL_IMPLICIT_GENERAL\n");

		str_tmp = "{0:>10}{1:>10g}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(imflag,self.dt,2,1,2,0,0,0);
		f.write(str_tmp);

		f.close();

	def Mem_print(self,path):

		mem = 200000000;
		ncpu = 8;

		f = open(path,'a');
		str_tmp = "*KEYWORD MEMORY={0} NCPU={1}\n".format(mem,ncpu);
		f.write(str_tmp);

		f.close();

	def Springback_print(self,path):

		psid = 1;
		
		f = open(path,'a');
		str_tmp = "*INTERFACE_SPRINGBACK_LSDYNA\n";
		f.write(str_tmp);

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(psid,0,0,0,0,0,0,0);
		f.write(str_tmp);

		f.close();

	def DatabaseBinary_print(self,path):

		dt = self.dt/self.n_output;
		
		f = open(path,'a');
		str_tmp = "*DATABASE_BINARY_D3PLOT\n";
		f.write(str_tmp);

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}\n".format(dt,0,0,0,0);
		f.write(str_tmp);
		str_tmp = "{0:>10}\n".format(0);
		f.write(str_tmp);

		f.close();

	def DatabaseBinaryDump_print(self,path):

		f = open(path,'a');
		str_tmp = "*DATABASE_BINARY_D3DUMP\n";
		f.write(str_tmp);

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}\n".format(self.restart_dt,0,0,0,0);
		f.write(str_tmp);

		f.close();

	def ControlAccuracy_print(self,path):

		f = open(path,'a');
		f.write("*CONTROL_ACCURACY\n");

		str_tmp = "{0:>10}{1:>10g}{2:>10}{3:>10}\n".format(1, 1, 1, 1);
		f.write(str_tmp);

		f.close();

	def ControlEnergy_print(self,path):

		f = open(path,'a');
		f.write("*CONTROL_ENERGY\n");

		str_tmp = "{0:>10}{1:>10g}{2:>10}{3:>10}\n".format(2, 1, 2, 1);
		f.write(str_tmp);

		f.close();

	def ControlHourglass_print(self,path):

		f = open(path,'a');
		f.write("*CONTROL_HOURGLASS\n");

		str_tmp = "{0:>10}{1:>10g}\n".format(1, 0.1);
		f.write(str_tmp);

		f.close();


	def Full_print(self,path):

		self.Mem_print(path);
		self.Termination_print(path);
		self.Timestep_print(path);
		self.Springback_print(path);
		self.DatabaseBinary_print(path);
		self.DatabaseBinaryDump_print(path);
		self.ControlAccuracy_print(path);
		self.ControlEnergy_print(path);
		self.ControlHourglass_print(path);

