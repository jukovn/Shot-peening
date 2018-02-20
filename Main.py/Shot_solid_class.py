from Node_class import Node
from Element_class import El_Brick8
from scipy.stats import uniform

class Shot(Node,El_Brick8):
	
	r = 0.0; # m
	
	rmin = 0.08e-3;
	rmax = 0.10e-3;

	nodes = [];
	nodes_num = 0;
	
	elements = [];
	elements_num = 0;

	x0 = 0.0; # m
	y0 = 0.0; # m
	z0 = 0.0;#0.45e-3 + r;#0.6e-3; # m

	Vx = 0; # m/c
	Vy = 0; # m/c
	Vz = -100.0; # m/c

	ro = 8220; # kg/m^3
	Ee = 2e11; # Pa
	pr = 0.3;  # - 

	CI_system = 1; # 1 - Ci system enabled (M,C,N,kg)
				   # 0 - CI system disabled (mm,C,N,ton)

	shot_num = 0;
	Data_path = '';

	time_birth = 0.0;
	time_death = 0.0;

	border = 0.0;

	targ_a = 0.0;
	targ_c = 0.0;



	def __init__(self,targ_a,targ_c,border,shot_num,birth_time,death_time,Data_path):

		# border = 0.25e-3;#1.05*self.rmax; # mm
		self.border = border;
		self.targ_a = targ_a;
		self.targ_c = targ_c;

		self.shot_num = shot_num;
		self.time_birth = birth_time;
		self.time_death = death_time;

		self.nodes = [];
		self.nodes_num = 0;
		
		self.elements = [];
		self.elements_num = 0;

		self.r = uniform.rvs(self.rmin , self.rmax - self.rmin);

		self.x0 = uniform.rvs((-targ_a/2 + border) , (targ_a -2*border));
		self.y0 = uniform.rvs((-targ_a/2 + border) , (targ_a - 2*border));
		self.z0 = 0.005e-3 + targ_c + self.r + abs(self.time_birth*self.Vz);

	


		self.Data_path = Data_path;


	def Var_corr(self):

		if self.CI_system == 0:

			self.r = self.r*1e3;

			self.x0 = self.x0*1e3;
			self.y0 = self.y0*1e3;
			self.z0 = self.z0*1e3;

			self.Vx = self.Vx*1e3;
			self.Vy = self.Vy*1e3;
			self.Vz = self.Vz*1e3;

			self.ro = self.ro*1e-12;
			self.Ee = self.Ee*1e-6;

	
	def Nodes_read(self,dir_path,init_node_num):

		path = self.Data_path + "Shot_solid.k";

		f = open(path,"r");

		str_tmp = "";
		while str_tmp.find('*NODE') == -1:
			str_tmp = f.readline();
		if str_tmp.find('*NODE') != -1:
			str_tmp = f.readline();

			while str_tmp.find('*') == -1:

				self.nodes_num = self.nodes_num + 1;

				node_tmp = Node();

				node_tmp.num = int(str_tmp[0:8]) + init_node_num;
				node_tmp.x = float(str_tmp[8:24]);
				node_tmp.y = float(str_tmp[24:40]);
				node_tmp.z = float(str_tmp[40:56]);

				self.nodes.append(node_tmp);

				# print node_num;

				str_tmp = f.readline();

		f.close();

	def Nodes_corr(self):

		for i in range(self.nodes_num):

			self.nodes[i].x = self.nodes[i].x*self.r/1.0 + self.x0;
			self.nodes[i].y = self.nodes[i].y*self.r/1.0 + self.y0;
			self.nodes[i].z = self.nodes[i].z*self.r/1.0 + self.z0;


	def Elem_read(self,dir_path,init_elem_num):

		path = self.Data_path + "Shot_solid.k";

		f = open(path,"r");

		str_tmp = "";
		while str_tmp.find('*ELEMENT_SOLID') == -1:
			str_tmp = f.readline();
		if str_tmp.find('*ELEMENT_SOLID') != -1:
			str_tmp = f.readline();

			while str_tmp.find('*') == -1:
				self.elements_num = self.elements_num + 1;
				elem_tmp = El_Brick8();

				elem_tmp.num = int(str_tmp[0:8]) + init_elem_num;
				elem_tmp.Add_Node( self.nodes[int(str_tmp[16:24]) - 1] );
				elem_tmp.Add_Node( self.nodes[int(str_tmp[24:32]) - 1] );
				elem_tmp.Add_Node( self.nodes[int(str_tmp[32:40]) - 1] );
				elem_tmp.Add_Node( self.nodes[int(str_tmp[40:48]) - 1] );
				elem_tmp.Add_Node( self.nodes[int(str_tmp[48:56]) - 1] );
				elem_tmp.Add_Node( self.nodes[int(str_tmp[56:64]) - 1] );
				elem_tmp.Add_Node( self.nodes[int(str_tmp[64:72]) - 1] );
				elem_tmp.Add_Node( self.nodes[int(str_tmp[72:80]) - 1] );

				self.elements.append(elem_tmp);

				# print elements[-1].nodes[0].num,elements[-1].nodes[1].num,elements[-1].nodes[2].num,elements[-1].nodes[3].num,elements[0].nodes[0].num,elements[0].nodes[1].num,elements[0].nodes[2].num,elements[0].nodes[3].num

				str_tmp = f.readline();

		f.close();


	def Nodes_print(self,path):
        
		f = open(path,'a');
		f.write("*NODE\n");
		tc = 0;
		rc = 0;
		for i in range(self.nodes_num):
		    str_tmp = "{0:>8}{1:>16g}{2:>16g}{3:>16g}{4:>8}{5:>8}\n".format(self.nodes[i].num,self.nodes[i].x,self.nodes[i].y,self.nodes[i].z,tc,rc);
		    f.write(str_tmp);

		f.close();

	def Elements_print(self,path):

		f = open(path,'a');
		f.write("*ELEMENT_SOLID\n");

		pid = 2 + self.shot_num;

		for i in range(self.elements_num):
		    str_tmp = "{0:>8}{1:>8}{2:>8}{3:>8}{4:>8}{5:>8}{6:>8}{7:>8}{8:>8}{9:>8}\n".format(self.elements[i].num,pid,self.elements[i].nodes[0].num,self.elements[i].nodes[1].num,self.elements[i].nodes[2].num,self.elements[i].nodes[3].num,self.elements[i].nodes[4].num,self.elements[i].nodes[5].num,self.elements[i].nodes[6].num,self.elements[i].nodes[7].num);
		    f.write(str_tmp);

		f.close();


	def SolidSection_print(self,path):
		if self.shot_num == 0:
			secid = 2;
			elform = 1;        

			f = open(path,'a');
			f.write("*SECTION_SOLID\n");
			str_tmp = "{0:>8}{1:>8}{2:>8}\n".format(secid,elform,0);
			f.write(str_tmp);


			f.close();


	# def Mat_solid_print(self,path):

	#     matid = 2;


	#     f = open(path,'a');
	#     f.write("*MAT_RIGID_TITLE\n");
	#     f.write("Rigid material\n")
	#     str_tmp = "{0:>10}{1:>10g}{2:>10g}{3:>10g}{4:>10}{5:>10}{6:>10}\n".format(matid,self.ro,self.Ee,self.pr,0.0,0.0,0.0);
	#     f.write(str_tmp);
	#     str_tmp = "{0:>10}{1:>10}{2:>10}\n".format(0.0,0,0);
	#     f.write(str_tmp);
	#     str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}\n".format(0.0,0.0,0.0,0.0,0.0,0.0);
	#     f.write(str_tmp);
	    
	    
	#     f.close();

	def Mat_elastic_print(self,path):
		if self.shot_num == 0:
			matid = 2;

			f = open(path,'a');
			f.write("*MAT_ELASTIC\n");
			str_tmp = "{0:>10}{1:>10g}{2:>10g}{3:>10g}{4:>10}{5:>10}{6:>10}\n".format(matid,self.ro,self.Ee,self.pr,0.0,0.0,0);
			f.write(str_tmp);


			f.close();



	def Part_print(self,path):

	    pid = 2 + self.shot_num;
	    secid = 2;
	    matid = 2;

	    f = open(path,'a');
	    f.write("*PART\n");
	    f.write("Shot\n")
	    str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(pid,secid,matid,0,0,0,0,0);
	    f.write(str_tmp);
	    
	    f.close();


	def Set_shot_nodes(self,path):

		sid = 4 + self.shot_num;

		f = open(path,'a');
		f.write("*SET_NODE_LIST_TITLE\n");
		f.write("Shot_node_list" + str(self.shot_num + 1) + "\n");
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}".format(sid,0.0,0.0,0.0,0.0);
		f.write(str_tmp);
		f.write("MECH\n")

		for i in range(int(self.nodes_num/8)):
		    for j in range(8):
		        str_tmp = "{0:>10}".format(self.nodes[i*8 + j].num);
		        f.write(str_tmp);
		    f.write("\n");

		if self.nodes_num%8 != 0:
		    for i in range(8):
		        if (int(self.nodes_num/8)*8 + i)<self.nodes_num:
		            str_tmp = "{0:>10}".format(self.nodes[int(self.nodes_num/8)*8 + i].num);
		            f.write(str_tmp);
		        else:
		            str_tmp = "{0:>10}".format(0);
		            f.write(str_tmp);
		    f.write("\n");






	# def InitVel_rigid_print(self,path): # 

	# 	pid = 2 + self.shot_num;

	# 	f = open(path,'a');
	# 	f.write("*INITIAL_VELOCITY_RIGID_BODY\n");
	# 	str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(pid,self.Vx,self.Vy,self.Vz,0.0,0.0,0.0,0);
	# 	f.write(str_tmp);

	# 	f.close();

	# def InitVelGen_print(self,path): #

	# 	pid = 2 + self.shot_num;
	# 	styp = 2;
	# 	omega = 0.0;

	# 	f = open(path,'a');
	# 	f.write("*INITIAL_VELOCITY_GENERATION\n");
	# 	str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(pid,styp,omega,self.Vx,self.Vy,self.Vz,0,0);
	# 	f.write(str_tmp);
	# 	str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(0.0,0.0,0.0,0.0,0.0,0.0,0,0);
	# 	f.write(str_tmp);

	# 	f.close();


	
	def InitVel_nodes_print(self,path): #

		nsid = 4 + self.shot_num;
		f = open(path,'a');

		f.write("*INITIAL_VELOCITY\n");
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}\n".format(nsid,0,0,0,0);
		f.write(str_tmp);
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}\n".format(self.Vx,self.Vy,self.Vz,0.0,0.0,0.0);
		f.write(str_tmp);

		f.close();

	# def VelocityCurve_print(self,path):

	# 	lcid = self.shot_num + 1;

	# 	f = open(path,'a');

	# 	f.write("*DEFINE_CURVE_TITLE\n");
	# 	f.write("Velocity curve" + str(lcid) + '\n');
	# 	str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(lcid,0,1.0,1.0,0.0,0.0,0,0);
	# 	f.write(str_tmp);




	# 	str_tmp = "{0:>20}{1:>20}\n".format(0.0,0.0);
	# 	f.write(str_tmp);
	# 	str_tmp = "{0:>20}{1:>20}\n".format(self.time_birth - 1e-8,0.0);
	# 	f.write(str_tmp);
	# 	str_tmp = "{0:>20}{1:>20}\n".format(self.time_birth ,1.0);
	# 	f.write(str_tmp);
	# 	str_tmp = "{0:>20}{1:>20}\n".format(self.time_birth + 1e-8 ,0.0);
	# 	f.write(str_tmp);
	# 	str_tmp = "{0:>20}{1:>20}\n".format(10000.0 ,0.0);
	# 	f.write(str_tmp);

	# 	f.close();


# *DEFINE_CURVE_TITLE
# Velocity curve 1
# $#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
#          1         0       1.0       1.0       0.0       0.0         0         0
# $#                a1                  o1  
#                  0.0                 0.0
#    3.9999999757e-008                 1.0
#    5.0000000584e-008                 0.0
#               1000.0                 0.0

# 	def BoundPrescrMotion_print(self,path):

# 		lcid = self.shot_num + 1;
# 		nsid = self.shot_num + 2;

# 		f = open(path,'a');

# 		f.write("*BOUNDARY_PRESCRIBED_MOTION_SET\n");
		
# 		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(nsid,3,0,lcid,self.Vz,0,100000,0.0);
# 		f.write(str_tmp);


# 		f.close();

# # *BOUNDARY_PRESCRIBED_MOTION_SET
# # $#    nsid       dof       vad      lcid        sf       vid     death     birth
# #          2         3         0         1    -100.0         01.00000E28       0.0

	def PartSet_print(self,path):

		sid = 2 + self.shot_num;
		part1_id = 1;
		part2_id = 2 + self.shot_num;

		f = open(path,'a');
		f.write("*SET_PART_LIST_TITLE\n");
		f.write("Contact pair set\n");
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}".format(sid,0.0,0.0,0.0,0.0);
		f.write(str_tmp + "MECH\n");

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(part1_id,part2_id,0,0,0,0,0,0);
		f.write(str_tmp);

		f.close();

	def ContactPar_print(self,path):

		cid = 3 + self.shot_num;
		ssid = 1;
		msid = 2 + self.shot_num;
		sstyp = 3;
		mstyp = 3;
		sboxid = 1;
		mboxid = 2 + self.shot_num;

		soft = 2;

		stat_fric_coef = 0.3;
		visc_damp_coef = 50;

		small_pen = 1;

		birth_time = self.time_birth;
		death_time = self.time_death;

		f = open(path,'a');
		#f.write("*CONTACT_AUTOMATIC_ONE_WAY_SURFACE_TO_SURFACE_ID\n");
		f.write("*CONTACT_AUTOMATIC_SURFACE_TO_SURFACE_ID\n");
		str_tmp = "{0:>10}".format(cid);
		f.write(str_tmp + "Contact\n");

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(ssid,msid,sstyp,mstyp,sboxid,mboxid,0,0);
		f.write(str_tmp);

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(stat_fric_coef,0.0,0.0,0.0,visc_damp_coef,small_pen,birth_time,death_time);
		f.write(str_tmp);

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(1.0,1.0,0.0,0.0,1.0,1.0,1.0,1.0);
		f.write(str_tmp);

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format(soft,0.1,0,1.025,2.0,2,0,1);
		f.write(str_tmp);

		f.close();

	def SolidElemSet_print(self,path):

		sid = 1 + self.shot_num;
		part_num = 2 + self.shot_num;

		f = open(path,'a');
		f.write("*SET_SOLID_GENERAL_TITLE\n");
		f.write("Shot" + str(sid) + "\n");
		str_tmp = "{0:>10}".format(sid);
		f.write(str_tmp + "MECH\n");

		str_tmp = "{0:<10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}\n".format("PART",part_num,0,0,0,0,0,0);
		f.write(str_tmp);

		f.close();

	def SolidElemDeath_print(self,path):

		sid = 1 + self.shot_num;

		f = open(path,'a');
		f.write("*DEFINE_ELEMENT_DEATH_SOLID_SET\n");
		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}\n".format(sid,self.time_death,0,0);
		f.write(str_tmp);

		f.close();

	def DefToRigid_print(self,path):

		pid = 2 + self.shot_num;

		f = open(path,'a');
		f.write("*DEFORMABLE_TO_RIGID\n");
		str_tmp = "{0:>10}{1:>10}\n".format(pid,0);
		f.write(str_tmp);

		f.close();



	def DefineBox_print(self,path):

		boxid = 2 + self.shot_num;

		xmin = -self.targ_a/2 + self.border - 0.1e-3;
		xmax = self.targ_a/2 - self.border + 0.1e-3;
		ymin = -self.targ_a/2 + self.border - 0.1e-3;
		ymax = self.targ_a/2 - self.border + 0.1e-3;
		zmin = self.targ_c - 0.05e-3 + abs(self.time_birth*self.Vz);
		zmax = self.targ_c + 0.02e-3 + abs(self.time_birth*self.Vz);

		f = open(path,'a');
		f.write("*DEFINE_BOX_TITLE\n");
		f.write("Shot" + str(self.shot_num + 1) + "contact_box\n");

		str_tmp = "{0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}\n".format(boxid,xmin,xmax,ymin,ymax,zmin,zmax);
		f.write(str_tmp);

		f.close();

	def DataInit(self,dir_path,init_node_num,init_elem_num):

		self.Nodes_read(dir_path,init_node_num)
		self.Nodes_corr();
		self.Elem_read(dir_path,init_elem_num);

	def Full_print(self,path):

		self.Var_corr();

		self.Nodes_print(path);
		self.Elements_print(path);
		self.SolidSection_print(path);
		
		self.Mat_elastic_print(path);
		
		self.Set_shot_nodes(path);
		self.Part_print(path);
		
		self.InitVel_nodes_print(path);


		self.PartSet_print(path);
		self.DefineBox_print(path);
		self.ContactPar_print(path);

		self.SolidElemSet_print(path);
		self.SolidElemDeath_print(path);
		# self.DefToRigid_print(path);
