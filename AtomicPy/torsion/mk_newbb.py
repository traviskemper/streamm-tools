#! /usr/bin/env python
# Make input files for torsional potential energy surface 

# Dr. Travis Kemper
# NREL
# 12/09/2013
# travis.kemper@nrel.gov

def get_options():
    import os, os.path
    from optparse import OptionParser
    usage = "usage: %prog [options] [input_files] \n"
    usage = usage + "Input files \n"
    usage = usage + "  specify the destination name of an option followed by the value"
    parser = OptionParser(usage=usage)
    

    parser.add_option("-v","--verbose", dest="verbose", default=True,action="store_true", help="Verbose output ")
    
    # Cluster options
    parser.add_option("--cluster_host", dest="cluster_host",type="string",default="peregrine",help=" name of cluster ")
    
    # QM calculation options 
    parser.set_defaults(qm_software="gaussian")
    parser.add_option("--qm_software", dest="qm_software",type="string",help=" what software to use for the qm calculations   ")
    

    # Output options 
    parser.add_option("--out_xyz", dest="out_xyz", type="string", default="", help="Output single frame xyz file in xmol format ")

    (options, args) = parser.parse_args()

    # Set options based on cluster 
    if( options.cluster_host == "peregrine" ):
        if( options.qm_software == "gaussian" ):
            options.qm_load = "module load gaussian/.g09_C.01"
    elif( options.cluster_host == "redmesa" ):
        if( options.qm_software == "gaussian" ):
            options.qm_load = "module load gaussian/g09/C.01"
	    
    return options, args


def build_nablist(ELN,BONDS):
    import sys,numpy

    debug = 0
    NNAB = 0

    maxnnab = len(BONDS)*2 + 1
    NBLIST = numpy.empty( maxnnab,  dtype=int )
    NBINDEX = numpy.empty( maxnnab,  dtype=int )

    if(debug ):
	for b in range( len(BONDS) ) :
	    bnd_i = BONDS[b][0]
	    bnd_j = BONDS[b][1]
	    print b, bnd_i,bnd_j
	    
    for i in range(len(ELN)):
	NBINDEX[i] = NNAB + 1
	for b in range( len(BONDS) ) :
	    bnd_i = BONDS[b][0]
	    bnd_j = BONDS[b][1]
	    if ( i == bnd_i ):
		NNAB = NNAB + 1
		NBLIST[NNAB] =  bnd_j
		if(debug): print " adding bnd_i",i,b,bnd_i,bnd_j,len(NBLIST),NBINDEX[i]
	
	    if ( i == bnd_j ):
		NNAB = NNAB + 1
		NBLIST[NNAB] =  bnd_i
		if(debug): print " adding bnd_j",i,b,bnd_i,bnd_j,len(NBLIST),NBINDEX[i]
		    
    #if(debug): sys.exit('debug')
    
    # Account for final atom position
    NBINDEX[i+1] =  NNAB + 1

    debug = 0
    if ( debug ):
       print ' total nbs ',NNAB,' total bonds ',len(BONDS)
       for i in range(len(ELN)):
	    N_o = NBINDEX[ i  ]
	    N_f = NBINDEX[ i + 1 ] - 1
	    NNAB = N_f - N_o + 1
	    print ' atom ', i,' ',ELN[i],NNAB,N_o
    
	    #
	    # Find number of elements
	    #
	    #ELCNT = numpy.zeros(120)
	    for indx in range( N_o,N_f+1):
		j = NBLIST[indx]
		print ELN[j],j
		#    el_j = ELN[j]
		#    ELCNT[j] = ELCNT[j] + 1

       sys.exit('mk_ff.build_nablist')


    return (NBLIST,NBINDEX)


    
def main():
    import sys, os 
    import string  , numpy  , json 
    from string import replace
    import file_io, gaussian, elements, gromacs, lammps , top, atom_types, xmol 
    
    options, args = get_options()
    
    if( options.cluster_host == "peregrine" ):
	load_gaussian = "module load gaussian/.g09_C.01 "
        user = 'tkemper'
	
    elif( options.cluster_host == "redmesa" ):
	load_gaussian = "module load gaussian/g09/C.01"
        user = 'twkempe'
	

    elif( options.cluster_host == "macbook" ):
	load_gaussian = ""
        user = 'tkemper'


	
    # sufix for force field calcs to run multiple ff types or excultions, such as q(i) = 0.00 
    ff_type_id = "_fit"
    
    LAT_CONST = numpy.zeros( (3,3) )
    
    LAT_CONST[0][0] = 50.0
    LAT_CONST[1][1] = 50.0
    LAT_CONST[2][2] = 50.0

    # Store working dir  
    work_dir = os.getcwd()
    
    # Read index files from args
    for indx_file in args:
        # Get lines of record file   
        f = open(indx_file,'r')
        Lines = f.readlines()
        f.close()
        for gen_line in Lines:
            col = gen_line.split()
            if( len(col) >= 4 and col[0] == "gen" ):
		
                mol_dir = col[1].strip()
                mol_id = col[2].strip()
                mol_repeat = int(col[3].strip() )
                mol_acc = col[4].strip()
                
                # File info
                struct_dir = mol_dir + "/" + mol_id + "/"
                job_name = mol_acc + "_" + mol_id + "_n" + str(mol_repeat)

		# Read data from json file
		json_name = struct_dir +"/" + job_name +".json"
		if(  file_io.file_exists( json_name) ):
		    if( options.verbose ):
			print "     Getting atomic data from  ",json_name
					    
		    f = open(json_name, 'r')
		    json_data = json.load(f)
		    f.close()
		    
		    ELN = []
		    ASYMB = []
		    ATYPE = []
		    CTYPE = []
		    CHARGES = []
		    R = []
		    CHARN = []
		    UNITNUMB = [] 
		    
		    natoms = json_data['metadata']["atomic"]["natoms"]  
		    print "       Number of atoms found in json file ",natoms
		    for atom_i in range( natoms ):
			ELN.append( json_data['metadata']["atomic"]["element"][atom_i]  )
			ASYMB.append( json_data['metadata']["atomic"]["asymb"][atom_i]  )
			ATYPE.append( json_data['metadata']["atomic"]["atype"][atom_i]  )
			CTYPE.append( json_data['metadata']["atomic"]["ctype"][atom_i]  )
			CHARGES.append( json_data['metadata']["atomic"]["q"][atom_i]  )
			CHARN.append( json_data['metadata']["atomic"]["qgroup"][atom_i]  )
			UNITNUMB.append( json_data['metadata']["atomic"]["unitnumb"][atom_i]  )
			pos_str = json_data['metadata']["atomic"]["pos"][atom_i].split()
			r_i = numpy.array( [float(pos_str[0]),float(pos_str[1]),float(pos_str[2])] )
			R.append( r_i )
		else:
		    print "   json file ",json_name," does not exist. "
		    sys.exit("error in json read  ")

		# Get geometry from optimized structure 
                calc_id = job_name
		log_file = struct_dir +'/' + calc_id +"/"+calc_id+".log"
		fchk_file = struct_dir +'/' + calc_id +"/"+calc_id+".fchk"
		
		opt_finished = 0 
		esp_finished = 0 
		if( file_io.file_exists( fchk_file) ):
                    if( options.verbose ):
			print  '    Get optimized geometry from ', fchk_file
			    
		    # Read in from zmatrix optimization 
		    NA, ELN, R, TOTAL_ENERGY, Q_ESP   = gaussian.parse_fchk( fchk_file )
		    
		    opt_finished = 1
		    # Update json data
		    #atomic_data["pos"] = []
		    for atom_i in range( len(ELN) ):				
			pos_str = str( "%f %f %f "% (R[atom_i][0],R[atom_i][1],R[atom_i][2]) )
			json_data['metadata']["atomic"]["pos"][atom_i] =  pos_str 
				
		    
				
		else:
		    print "  could not find ",fchk_file

		    
		# Get ESP chages 
		calc_id_esp = job_name + "-ESP"
		#    input_file = calc_id_esp + ".com"
		#    log_file_esp = struct_dir +'/' + calc_id_esp +"/"+calc_id_esp+".log"
		fchk_file_esp = struct_dir +'/' + calc_id_esp +"/"+calc_id_esp+".fchk"
		    
		if( file_io.file_exists( fchk_file_esp) ):
                    
		    if( options.verbose ):
			print "    Getting charges from esp fit ",fchk_file_esp
		    NA, ELN, R, TOTAL_ENERGY , CHARGES  = gaussian.parse_fchk( fchk_file_esp )

				
		else:
		    print "  could not find ",fchk_file_esp

		    
		#   Build covalent nieghbor list for bonded information 
		NBLIST, NBINDEX = top.build_covnablist(ELN,R)
		
		#
		# Set cply_tag for cply output
		#
		cply_tag = top.set_cply_tags(  options.verbose, ELN, CTYPE ,NBLIST, NBINDEX )
		#
		# Print new building block with charges 
		#
		
		if( options.verbose): print "    Creating BuildingBlock_local directories "
		bb_dir = struct_dir + "BuildingBlock_local"
		if (not os.path.isdir(bb_dir)):
		    os.mkdir(bb_dir)
		    
		for bb_subdir in ( "acceptors","donors","functional_groups","spacers","terminals" ):
		    mk_dir  = bb_dir +"/"+bb_subdir
		    if (not os.path.isdir(mk_dir)):
			os.mkdir(mk_dir)
		    
		bb_dir_donor =  struct_dir + "BuildingBlock_local/donors"
		    
		bb_file = bb_dir_donor +"/" + job_name + ".cply"
		
		if( options.verbose): print "    Creating BuildingBlock_local file ",bb_file
		
		F = open(bb_file,'w')
		F.write('D()')
		for atom_i in range( len(ELN) ):
		    F.write('\n %s %16.6f %16.6f %16.6f %s ' % (ASYMB[atom_i],R[atom_i][0],R[atom_i][1],R[atom_i][2],str( cply_tag[atom_i]) ) )			
		F.close()
		

		    
		os.chdir(work_dir)

if __name__=="__main__":
    main() 
