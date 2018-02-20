from Node_class import Node
from Element_class import El_Brick8
from copy import  copy
from numpy import linspace

class Target(Node,El_Brick8):
	
	a = 0.6e-3; # m
	b = 0.6e-3; # m
	c = 0.5e-3; # m

	dx = 10e-6; # m 6 
	dy = 10e-6; # m 6
	dz0 = 4e-6; # m 3
	bias_z = 1.3;

	ro = 8220;#7800; # kg/m^3
	Ee = 2e11; # Pa
	pr = 0.3; # -

	A = 460e6;#350e6; # Pa
	B = 1700e6;#275e6; # Pa
	N = 0.65;#0.36; # - 
	C = 0.017;#0.022; # - 
	Eps0 = 0.001;#1.0; # - 

	# Inconel 718 parameters from Joshi D. Finite Element Simulation of Machining a Nickel-based Superalloy-Inconel 718

	CI_system = 1; # 1 - Ci system enabled (M,C,N,kg)
				   # 0 - CI system disabled (mm,C,N,ton)

	nodes = [];
	nodes_num = 0;
	
	x_lev_num = 0;
	y_lev_num = 0;
	z_lev_num = 0;
	
	elements = [];
	elements_num = 0;

	bounded_nodes_z_num = 0;
	bounded_nodes_z = [];

	bounded_nodes_x_num = 0;
	bounded_nodes_x = [];

	bounded_nodes_y_num = 0;
	bounded_nodes_y = [];

	# output target data
	
	sig_diag_depth = 0.4e-3; ##in mm
	num_z_level = 200;
	num_xy_level = 9; # only odd numbers!

	a_p = (a - 0.55e-3)/2.0;
	b_p = (b - 0.55e-3)/2.0;
	c_p = c;

	x_p = [];
	y_p = [];
	z_p = [];

	border = a/2.0*(1.00 - 1.0/6.0);

	def __init__(self):

		self.nodes = [];
		self.nodes_num = 0;
		
		self.x_lev_num = 0;
		self.y_lev_num = 0;
		self.z_lev_num = 0;
		
		self.elements = [];
		self.elements_num = 0;

		self.bounded_nodes_z_num = 0;
		self.bounded_nodes_z = [];

		bounded_nodes_x_num = 0;
		bounded_nodes_x = [];

		bounded_nodes_y_num = 0;
		bounded_nodes_y = [];


	def Var_corr(self):

		if self.CI_system == 0:

			self.a = self.a*1e3;
			self.b = self.b*1e3;
			self.c = self.c*1e3;

			self.dx = self.dx*1e3;
			self.dy = self.dy*1e3;
			self.dz0 = self.dz0*1e3;

			self.ro = self.ro*1e-12;
			self.Ee = self.Ee*1e-6;
			self.A = self.A*1e-6;
			self.B = self.B*1e-6;


	def Grid_creation(self):
				
		dz_ar = [];

		z_sum = 0;
		n = 0;
		while (z_sum < self.c):
			z_sum = z_sum + self.dz0*self.bias_z**n;
			if (z_sum>self.c):
				dz_ar.append(self.dz0*self.bias_z**n - abs(z_sum-self.c))
			else:
				dz_ar.append(self.dz0*self.bias_z**n);
			n = n+1;
		
		dz_ar.reverse();
		
		z_ar = [0.0];
		for i in range(len(dz_ar)):
			z_ar.append(z_ar[i] + dz_ar[i]);
		
		
		x0 = -self.a/2;
		y0 = -self.a/2;
		# z0 = 0.0;
		
		self.x_lev_num = int(round(self.a/self.dx)) + 1;
		self.y_lev_num = int(round(self.b/self.dy)) + 1;
		self.z_lev_num = int(len(dz_ar) + 1);
		
		# target_nodes = [];
		curr_num = 1;
		
		for k in range(self.z_lev_num):
			for j in range(self.y_lev_num):
				for i in range(self.x_lev_num):
					
					node_temp = Node();
					node_temp.x = x0 + i*self.dx;
					node_temp.y = y0 + j*self.dy;
					node_temp.z = z_ar[k];
					node_temp.num = curr_num;
					
					self.nodes.append(node_temp);
		
					curr_num = curr_num + 1;
					
		self.nodes_num = self.nodes[-1].num;
		
	def Nodes_print(self,path):

		f = open(path,'a');
		
		f.write("*NODE\n");
		tc = 0;
		rc = 0;
		for i in range(self.nodes_num):
			str_tmp = "{0:>8}{1:>16g}{2:>16g}{3:>16g}{4:>8}{5:>8}\n".format(self.nodes[i].num,self.nodes[i].x,self.nodes[i].y,self.nodes[i].z,tc,rc);
			f.write(str_tmp);
		
		f.close();
		
	def Elements_creation(self):
		
		curr_num = 1;
		for k in range(self.z_lev_num - 1):
			for j in range(self.y_lev_num - 1):
				for i in range(self.x_lev_num - 1):
					# self.elements.append(El_Brick8());
					el_tmp = El_Brick8();
					self.elements.append(el_tmp);


					self.elements[curr_num-1].num = curr_num;
					
					# print curr_num, self.elements[curr_num-1].node1.num, self.elements[curr_num-1].node5.num, self.elements[curr_num-1].curr_node_num, len(self.elements)

					curr_num = curr_num + 1;


					
		self.elements_num = self.elements[-1].num;
		
		z_lvl = self.x_lev_num*self.y_lev_num;
		curr_num = 1;
		for k in range(self.z_lev_num - 1):
			for j in range(self.y_lev_num - 1):
				for i in range(self.x_lev_num - 1):
					
					# print "NODES = ",self.nodes[0].num,self.nodes[2602].num,z_lvl*(k+1) + self.y_lev_num*j + (i+1);
					# print self.elements[curr_num-1].curr_node_num,self.elements[curr_num-1].node4.num;
					
					self.elements[curr_num-1].Add_Node(self.nodes[z_lvl*(k+1) + self.y_lev_num*j + (i+1)]);
					self.elements[curr_num-1].Add_Node(self.nodes[z_lvl*(k+1) + self.y_lev_num*j + (i)]);
					self.elements[curr_num-1].Add_Node(self.nodes[z_lvl*(k) + self.y_lev_num*j + (i)]);
					self.elements[curr_num-1].Add_Node(self.nodes[z_lvl*(k) + self.y_lev_num*j + (i+1)]);
					self.elements[curr_num-1].Add_Node(self.nodes[z_lvl*(k+1) + self.y_lev_num*(j+1) + (i+1)]);
					self.elements[curr_num-1].Add_Node(self.nodes[z_lvl*(k+1) + self.y_lev_num*(j+1) + (i)]);
					self.elements[curr_num-1].Add_Node(self.nodes[z_lvl*(k) + self.y_lev_num*(j+1) + (i)]);
					self.elements[curr_num-1].Add_Node(self.nodes[z_lvl*(k) + self.y_lev_num*(j+1) + (i+1)]);
					
					# self.elements[curr_num-1].nodes.append(self.nodes[z_lvl*(k+1) + self.y_lev_num*j + (i+1)]);
					# self.elements[curr_num-1].nodes.append(self.nodes[z_lvl*(k+1) + self.y_lev_num*j + (i)]);
					# self.elements[curr_num-1].nodes.append(self.nodes[z_lvl*(k) + self.y_lev_num*j + (i)]);
					# self.elements[curr_num-1].nodes.append(self.nodes[z_lvl*(k) + self.y_lev_num*j + (i+1)]);
					# self.elements[curr_num-1].nodes.append(self.nodes[z_lvl*(k+1) + self.y_lev_num*(j+1) + (i+1)]);
					# self.elements[curr_num-1].nodes.append(self.nodes[z_lvl*(k+1) + self.y_lev_num*(j+1) + (i)]);
					# self.elements[curr_num-1].nodes.append(self.nodes[z_lvl*(k) + self.y_lev_num*(j+1) + (i)]);
					# self.elements[curr_num-1].nodes.append(self.nodes[z_lvl*(k) + self.y_lev_num*(j+1) + (i+1)]);
					
					
					# print self.nodes[z_lvl*(k+1) + self.y_lev_num*j + (i+1)].num;
					# print curr_num,self.elements[curr_num-1].nodes[0].num;
					
					curr_num = curr_num + 1;

		
	def Elements_print(self,path):
		
		f = open(path,'a');
		f.write("*ELEMENT_SOLID\n");
		
		pid = 1;
		
		for i in range(self.elements_num):
			str_tmp = "{0:>8}{1:>8}{2:>8}{3:>8}{4:>8}{5:>8}{6:>8}{7:>8}{8:>8}{9:>8}\n".format(self.elements[i].num,pid,self.elements[i].nodes[0].num,self.elements[i].nodes[1].num,self.elements[i].nodes[2].num,self.elements[i].nodes[3].num,self.elements[i].nodes[4].num,self.elements[i].nodes[5].num,self.elements[i].nodes[6].num,self.elements[i].nodes[7].num);
			f.write(str_tmp);
		
		f.close();
		
	def SolidSection_print(self,path):

		secid = 1;
		elform = 1; # 1 - 8 node element with 1 integration point 

		f = open(path,'a');
		f.write("*SECTION_SOLID\n");
		str_tmp = "{0:>8}{1:>8}{2:>8}\n".format(secid,elform,0);
		f.write(str_tmp);
		
		
		f.close();

	def Mat_print(self,path):

		matid = 1;


		f = open(path,'a');
		f.write("*MAT_SIMPLIFIED_JOHNSON_COOK_TITLE\n");
		f.write("Johnson Cook simplified\n")
		str_tmp = "{0:>10}{1:>10g}{2:>10g}{3:>10g}{4:>10}\n".format(matid,self.ro,self.Ee,self.pr,0);
		f.write(str_tmp);
		str_tmp = "{0:>10g}{1:>10g}{2:>10g}{3:>10g}{4:>10g}{5:>10g}{6:>10g}{7:>10g}\n".format(self.A,self.B,self.N,self.C,1e17,1e28,1e28,self.Eps0);
		f.write(str_tmp);
		
		
		f.close();

	def Hourglass_print(self,path):

		hgid = 1;

		f = open(path,'a');
		f.write("*HOURGLASS\n");
		str_tmp = "{0:>10g}{1:>10g}{2:>10g}{3:>10g}{4:>10g}{5:>10g}{6:>10g}{7:>10g}\n".format(hgid, 5, 0.1, 0, 1.5, 0.06, 0.1, 0.1);
		f.write(str_tmp);
		
		
		f.close();


	def Part_print(self,path):

		pid = 1;
		secid = 1;
		matid = 1;
		hgid = 1;

		f = open(path,'a');
		f.write("*PART\n");
		f.write("Target\n")
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(pid,secid,matid,0,hgid,0,0,0);
		f.write(str_tmp);
		
		f.close();

	def Bounded_nodes_z_define(self):

		for i in range(self.nodes_num):
			if self.nodes[i].z == 0:

				self.bounded_nodes_z.append(self.nodes[i]);
				self.bounded_nodes_z_num = self.bounded_nodes_z_num + 1;

	def Bounded_nodes_x_define(self):

		for i in range(self.nodes_num):
			if ( (self.nodes[i].x < (self.a/2 + self.dx/2)) and ((self.nodes[i].x > (self.a/2 - self.dx/2))) ) or ( (self.nodes[i].x < (-self.a/2 + self.dx/2)) and ((self.nodes[i].x > (-self.a/2 - self.dx/2))) ):

				self.bounded_nodes_x.append(self.nodes[i]);
				self.bounded_nodes_x_num = self.bounded_nodes_x_num + 1;

	def Bounded_nodes_y_define(self):

		for i in range(self.nodes_num):
			if ( (self.nodes[i].y < (self.b/2 + self.dy/2)) and ((self.nodes[i].y > (self.b/2 - self.dy/2))) ) or ( (self.nodes[i].y < (-self.b/2 + self.dy/2)) and ((self.nodes[i].y > (-self.b/2 - self.dy/2))) ):

				self.bounded_nodes_y.append(self.nodes[i]);
				self.bounded_nodes_y_num = self.bounded_nodes_y_num + 1;


	def Bounded_nodes_z_print(self,path):

		sid = 1;
		f = open(path,'a');
		f.write("*SET_NODE_LIST_TITLE\n");
		f.write("bound_node_z_list\n");
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}".format(sid,0.0,0.0,0.0,0.0);
		f.write(str_tmp);
		f.write("MECH\n")

		for i in range(int(self.bounded_nodes_z_num/8)):
			for j in range(8):
				str_tmp = "{0:>10}".format(self.bounded_nodes_z[i*8 + j].num);
				f.write(str_tmp);
			f.write("\n");

		if self.bounded_nodes_z_num%8 != 0:
			for i in range(8):
				if (int(self.bounded_nodes_z_num/8)*8 + i)<self.bounded_nodes_z_num:
					str_tmp = "{0:>10}".format(self.bounded_nodes_z[int(self.bounded_nodes_z_num/8)*8 + i].num);
					f.write(str_tmp);
				else:
					str_tmp = "{0:>10}".format(0);
					f.write(str_tmp);
			f.write("\n");

	def Bounded_nodes_x_print(self,path):

		sid = 2;
		f = open(path,'a');
		f.write("*SET_NODE_LIST_TITLE\n");
		f.write("bound_node_x_list\n");
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}".format(sid,0.0,0.0,0.0,0.0);
		f.write(str_tmp);
		f.write("MECH\n")

		for i in range(int(self.bounded_nodes_x_num/8)):
			for j in range(8):
				str_tmp = "{0:>10}".format(self.bounded_nodes_x[i*8 + j].num);
				f.write(str_tmp);
			f.write("\n");

		if self.bounded_nodes_x_num%8 != 0:
			for i in range(8):
				if (int(self.bounded_nodes_x_num/8)*8 + i)<self.bounded_nodes_x_num:
					str_tmp = "{0:>10}".format(self.bounded_nodes_x[int(self.bounded_nodes_x_num/8)*8 + i].num);
					f.write(str_tmp);
				else:
					str_tmp = "{0:>10}".format(0);
					f.write(str_tmp);
			f.write("\n");


	def Bounded_nodes_y_print(self,path):

		sid = 3;
		f = open(path,'a');
		f.write("*SET_NODE_LIST_TITLE\n");
		f.write("bound_node_y_list\n");
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}".format(sid,0.0,0.0,0.0,0.0);
		f.write(str_tmp);
		f.write("MECH\n")

		for i in range(int(self.bounded_nodes_y_num/8)):
			for j in range(8):
				str_tmp = "{0:>10}".format(self.bounded_nodes_y[i*8 + j].num);
				f.write(str_tmp);
			f.write("\n");

		if self.bounded_nodes_y_num%8 != 0:
			for i in range(8):
				if (int(self.bounded_nodes_y_num/8)*8 + i)<self.bounded_nodes_y_num:
					str_tmp = "{0:>10}".format(self.bounded_nodes_y[int(self.bounded_nodes_y_num/8)*8 + i].num);
					f.write(str_tmp);
				else:
					str_tmp = "{0:>10}".format(0);
					f.write(str_tmp);
			f.write("\n");

	def BoundaryConstrZ_print(self,path):

		NSID = 1;

		f = open(path,'a');
		f.write("*BOUNDARY_SPC_SET_ID\n");
		str_tmp = "{0:>10}".format(0);
		f.write(str_tmp);
		f.write("Boundary_Z\n")
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(NSID,0,1,1,1,1,1,1);
		f.write(str_tmp);
		
		f.close();

	def BoundaryConstrX_print(self,path):

		NSID = 2;

		f = open(path,'a');
		f.write("*BOUNDARY_SPC_SET_ID\n");
		str_tmp = "{0:>10}".format(0);
		f.write(str_tmp);
		f.write("Boundary_X\n")
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(NSID,0,1,0,0,0,0,0);
		f.write(str_tmp);
		
		f.close();

	def BoundaryConstrY_print(self,path):

		NSID = 3;

		f = open(path,'a');
		f.write("*BOUNDARY_SPC_SET_ID\n");
		str_tmp = "{0:>10}".format(0);
		f.write(str_tmp);
		f.write("Boundary_Y\n")
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(NSID,0,0,1,0,0,0,0);
		f.write(str_tmp);
		
		f.close();


	def PartSet_print(self,path):

		sid = 1;
		part1_id = 1;

		f = open(path,'a');
		f.write("*SET_PART_LIST_TITLE\n");
		f.write("Target set\n");
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}".format(sid,0.0,0.0,0.0,0.0);
		f.write(str_tmp + "MECH\n");

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(part1_id,0,0,0,0,0,0,0);
		f.write(str_tmp);

		f.close();


	def ResPointGrid_print(self,dir_path):

		# path = dir_path + "Prog_files\\Output_points.dat";
		path = dir_path + "Output_points.dat";

		points_num = self.num_xy_level*self.num_xy_level*self.num_z_level;

		self.x_p = linspace(-self.a_p,self.a_p,self.num_xy_level);
		self.y_p = linspace(-self.b_p,self.b_p,self.num_xy_level);
		self.z_p = linspace(self.c_p,self.c_p - self.sig_diag_depth,self.num_z_level);

		f1 = open(path,'w');

		f1.write(str(points_num) + ' ' + str(self.num_xy_level) + ' ' + str(self.num_xy_level) + ' ' + str(self.num_z_level) + '\n');

		for i in range(self.num_xy_level):
			for j in range(self.num_xy_level):
				for k in range(self.num_z_level):

					f1.write(str(self.x_p[i]) + ' ' + str(self.y_p[j]) + ' ' + str(self.z_p[k]) + '\n');

		f1.close();
 

	def DefineBox_print(self,path):

		boxid = 1;

		xmin = -self.a/2 + self.border - 0.1e-3;
		xmax = self.a/2 - self.border + 0.1e-3;
		ymin = -self.a/2 + self.border - 0.1e-3;
		ymax = self.a/2 - self.border + 0.1e-3;
		zmin = self.c - 0.05e-3;
		zmax = self.c + 0.02e-3;

		f = open(path,'a');
		f.write("*DEFINE_BOX_TITLE\n");
		f.write("Target contact_box\n");

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}\n".format(boxid,xmin,xmax,ymin,ymax,zmin,zmax);
		f.write(str_tmp);

		f.close();


	def FirstDataInit(self,dir_path):

		self.Grid_creation()
		self.Elements_creation();
		self.ResPointGrid_print(dir_path);

		self.Bounded_nodes_z_define();
		self.Bounded_nodes_x_define();
		self.Bounded_nodes_y_define();


	def Full_print(self,path):

		self.Var_corr();

		self.Nodes_print(path);
		self.Elements_print(path);
		self.SolidSection_print(path);
		self.Mat_print(path);
		self.Hourglass_print(path);
		self.Part_print(path);
		self.Bounded_nodes_z_print(path);
		self.Bounded_nodes_x_print(path);
		self.Bounded_nodes_y_print(path);
		self.BoundaryConstrZ_print(path);
		self.BoundaryConstrX_print(path);
		self.BoundaryConstrY_print(path);
		self.PartSet_print(path);
		self.DefineBox_print(path);