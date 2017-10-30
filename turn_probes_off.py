import xml.etree.ElementTree as ET
from bokeh.server.start import stop

class edit_design_file():
    def __init__(self):
        # define input array xml files
        self.old_array_design="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\array_design_028469\\028469_Guys19_110601.xml"
        self.new_array_design="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\array_design_085030\\CGH 4.3_085030_D_F_20170809_Guys19.xml"
        
        # new bedfile
        self.new_array_design_bedfile="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\array_design_085030\\CGH 4.3_085030_D_BED_20170809.bed"
        
        # set output files
        self.filtered_array_design="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\dev\\CGH 4.3_085030_D_F_20170809_Guys19_FILTERED.xml"
        self.filtered_array_design_bedfile="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\dev\\CGH 4.3_085030_D_BED_20170809_FILTERED.bed"
        
        # add to the array design name
        self.name_to_modify_design_name="_filtered"
        
    def get_probe_list(self,xml_input_file):
        '''this function takes a single array design and returns a list of probe names'''
        # empty list to hold all probes in this design
        probe_list=[]
   
        #load the xml file into python object
        tree=ET.parse(xml_input_file)
        # set the root of the file
        root=tree.getroot()
        
        #loop through the file, looking at each 'reporter' section (each reporter section is a probe)
        for probe in root.iter('reporter'):
            # add the probe name to the list
            probe_list.append(probe.attrib['name'])
        #return list
        return probe_list
    
    def rewrite_control_file(self, oldprobelist, file_to_filter):
        '''this function takes the lists of probes that are to be 'turned off from the new array design and rewrites the xml file'''
        
        #load the xml file into python object
        tree=ET.parse(file_to_filter)
        
        # set the root of the file
        root=tree.getroot()
        
        #loop through the file, looking at each 'reporter' section (each reporter section is a probe)
        for probe in root.iter('reporter'):
            #if the probe name is not in the old array design
            if probe.attrib['name'] not in oldprobelist:
                # add a flag to ignore the probe
                probe.attrib['control_type']="ignore"       
                
        #write the new modified design to file 
        tree.write(self.filtered_array_design)
        
        #### Also need to write in some non-xml lines (comments and doc type)
        
        # open the filtered xml file created above 
        with open(self.filtered_array_design,'r') as filtered_no_header_file:
            
            # create a list of all the lines in this file so we can insert lines in as required
            filtered_no_header_list=filtered_no_header_file.readlines()
        
        # open the original array design file to get the non-xml lines 
        with open(self.new_array_design,'r') as new_array_design_file:
            # capture the top 50 lines into a list
            top_50_lines=[next(new_array_design_file) for x in xrange(50)]
        
        # the top 50 lines of both files should be the same (excluding any flags to ignore the probes)
        # we only want the non-xml stuff which occurs before the first xml tag which is 'project'
        # loop through each item in the enumerated list of top 50 lines
        for number,line in enumerate(top_50_lines):
            # set a flag so once we have reached the project tag we can stop
            stop=False
            # when we reach the project tag, change the stop variable to true
            if line.startswith("<project"):
                stop=True
            # if we haven't reached the xml yet, add the non-xml line into the same place in the filtered xml file list
            elif not stop:
                filtered_no_header_list.insert(number,line)
            # if we have already reached the xml pass over
            else:
                pass
        
        # re-write the list with the non-xml added in to file.
        with open(self.filtered_array_design,'w') as filtered_file_with_header:
            filtered_file_with_header.writelines(filtered_no_header_list)
    
    def create_new_bedfile(self, old_probes):
        '''This function takes the list of probes on the old array design as an input. It then opens the array_design bedfile in a list, loops through it assessing if the probe name is on the old array design. if it is the line is written to a new bedfile.'''
        # open the new array design bedfile
        with open(self.new_array_design_bedfile,'r') as inputbedfile:
            # put into a list
            bedfile_list=inputbedfile.readlines()
        # open a new file to write to
        with open(self.filtered_array_design_bedfile,'w') as filtered_bed:
            # for line in bed file
            for line in bedfile_list:
                # split the bedfile on tab, take the 4th column and remove any new line characters
                probename=line.split('\t')[3].rstrip()
                # if the probe name is on the old array write to the new bedfile
                if probename in set(old_probes):
                    filtered_bed.write(line)
            
    
               
        
           
    def what_to_do(self):
        '''This function uses the above modules to create the new array file'''
        # get lists of probes from new and old array designs
        old_probelist=self.get_probe_list(self.old_array_design) 
        #new_probelist=self.get_probe_list(self.new_array_design)
        
        # call function to write a design file where new probes have been filtered
        self.rewrite_control_file(old_probelist, self.new_array_design)
        
        ########################################################################
        # # count the number of probes to be excluded
        # in_both_count=0
        # new_probe=0
        # for probe in new_probelist:
        #     if probe in set(old_probelist):
        #         in_both_count+=1
        #     else:
        #         new_probe+=1
        # 
        ########################################################################
        
        #create the bed file 
        self.create_new_bedfile(old_probelist)
        
        ########################################################################
        # #print some probe counts etc
        # #print "probes on new design" + str(len(new_probelist))
        # #print "probes on old design" + str(len(old_probelist))
        # print "probes on both = "+str(in_both_count)
        # print "new probes to be excluded = "+str(new_probe)
        # #assert new_probelist==in_both_count+new_probe
        # print self.to_be_ignored[0:50]
        ########################################################################

        
        
#create instance of class        
go=edit_design_file()
#call function
go.what_to_do()
