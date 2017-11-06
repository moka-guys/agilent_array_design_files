import xml.etree.ElementTree as ET

class FilterArrayDesign():
    """
    This class takes two array designs, an "old" design and a "new" design. The new design may not yet be ISO accredited so only the accredited probes can be used.
    Array designs are in the form of xml files, where each probe are wrapped in a 'reporter' tag. There are different types of probes, including control probes which can be excluded from any analysis.
    This script takes all the probes from the accredited old design and uses this to turn any probes on the new design into control probes, in effect turning the probes off.
    The output is a "filtered" version of the "new" array design. 
    
    The script also creates a modified bedfile for the "new" design, removing any probes from the "new" design bed file which don't appear on the "old" array design 
    """
    
    def __init__(self):
        """Specify the input and output files"""
        # input xml file for "old" design
        self.old_array_design_xml="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\array_design_028469\\028469_Guys19_110601.xml"
        # input xml file for "new" design
        self.new_array_design_xml="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\array_design_084720\\CGH 4.2_084720_D_F_20170309.xml"
        
        # input bedfile for "new" design
        self.new_array_design_bedfile="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\array_design_085030\\CGH 4.3_085030_D_BED_20170809.bed"
        
        # output xml file for "filtered" design
        self.filtered_array_design_xml="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\filtered_new_design\\CGH 4.2_084720_D_F_20170309_FILTERED.xml"
        # output bedfile for "filtered" design
        self.filtered_array_design_bedfile="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\filtered_new_design\\ignore_me.bed"
        
                
    def get_probe_list(self,xml_input_file):
        """this function takes a single array design and returns a list of probe names"""
        # an empty list to hold all probes that will be identified when parsing the input design file
        probe_list=[]
   
        # Using the Element tree module parse the input xml file into python object
        tree=ET.parse(xml_input_file)
        
        # set the root of the xml tree so we can use this to loop
        root=tree.getroot()
        
        #loop through the file, looking at each 'reporter' section (each reporter section is a probe)
        for probe in root.iter('reporter'):
            # add the probe name to the list
            probe_list.append(probe.attrib['name'])
        
        #return list of probes
        return probe_list
    
    def add_controltype_to_new_probes(self, old_probe_list, file_to_filter):
        """
        This function recieves the list of probes on the 'old' array design and the file path to the 'new' array design
        The 'new' array XML design file is read into a python object and each probe is assessed. If the probe is not present in the 'old' array design it has an attribute of 
        control_type = ignore added to 'turn off' the probe
        The modified XML is then written to the 'filtered' array design file however this does not include non-XML data in the file such as the file type and header   
        """
        
        # load the xml file input to this function into a python object using the element tree package
        tree=ET.parse(file_to_filter)
        
        # set the root of the file
        root=tree.getroot()
        
        # loop through the file, looking at each 'reporter' section (each reporter section is a probe)
        for probe in root.iter('reporter'):
            #if the probe name is not in the old array design
            if probe.attrib['name'] not in old_probe_list:
                # add a flag to ignore the probe
                probe.attrib['control_type']="ignore"       
                
        # write the modified XML data object to the filtered XML output file.
        tree.write(self.filtered_array_design_xml)
        
                
    def add_non_XML_to_XML_file(self):
        """
        Some non-XML lines are required to be added to the 'filtered' file in order for the design file to be recognised by the scanner.
        These are found at the top of the XML file, before the project tag (usually around 10 lines).
        The top 50 lines of the 'New' array design XML file are read into a list
        The 'filtered' XML file is read back into a list and any lines before the project tag added into this list
        This list is then written back to file
        """
        # open the filtered XML file created above 
        with open(self.filtered_array_design_xml,'r') as filtered_xml_file_no_header:
            # create a list of all the lines in this file so we can insert lines in as required
            filtered_xml_file_no_header_list=filtered_xml_file_no_header.readlines()
        
        # open the original array design file to get the non-xml lines 
        with open(self.new_array_design_xml,'r') as new_array_design_file:
            # capture the top 50 lines into a list (this should include all the non-XML lines)
            top_50_lines=[next(new_array_design_file) for x in xrange(50)]
        
        
        # capture the first line of the 'filtered' XML file. This can be used to only bring in lines from the 'new' XML design before the XML which has already been captured 
        # take the start of the line (<project) only as the order of the other tags can change
        where_to_stop=str(filtered_xml_file_no_header_list[0][0:8])
        
        # set a flag so once we have reached the project tag we can stop
        stop_flag=False
        
        # loop through the list of lines from the 'new' array design. use enumerate so we can insert the lines into the list at the specific line 
        for number,line in enumerate(top_50_lines):
            # when we reach the project tag, change the StopFlag variable to true
            if where_to_stop in line:
                # set the tag to true
                stop_flag=True
            # if we haven't reached the xml yet, add the non-xml line into the same place in the filtered xml file list
            elif not stop_flag:
                filtered_xml_file_no_header_list.insert(number,line)
            # if we have already reached the xml pass
            else:
                pass
        
        # re-write the list with the non-xml added in to file.
        with open(self.filtered_array_design_xml,'w') as filtered_file_with_header:
            filtered_file_with_header.writelines(filtered_xml_file_no_header_list)
    
    def create_new_bedfile(self, old_probes):
        """
        This function takes the list of probes on the 'old' array design as an input. 
        It then opens the 'new' array_design bedfile in a list, loops through it assessing if the probe name is on the 'old' array design. 
        If it is the line is written to the 'filtered' bedfile.
        """
        # open the new array design bedfile
        with open(self.new_array_design_bedfile,'r') as input_bedfile:
            # put into a list
            bedfile_list=input_bedfile.readlines()
        
        # open a new file to write 'filtered' bed file
        with open(self.filtered_array_design_bedfile,'w') as filtered_bed:
            # for line in bed file
            for line in bedfile_list:
                # split the bedfile on tab, take the 4th column and remove any new line characters
                probe_name=line.split('\t')[3].rstrip()
                # if the probe name is on the old array write to the new bedfile
                if probe_name in set(old_probes):
                    filtered_bed.write(line)
            

def main():
    """
    This function calls modules from the FilterArrayDesign class
    """
    #create instance of class
    FilterArray=FilterArrayDesign()
    # Create a list for all probes on the old array design
    old_probe_list=FilterArray.get_probe_list(FilterArray.old_array_design_xml) 
    # Create a file containing the probes which have been 'turned off'
    FilterArray.add_controltype_to_new_probes(old_probe_list, FilterArray.new_array_design_xml)
    # add in any non-XML lines to the 'filtered' XML file
    FilterArray.add_non_XML_to_XML_file()
    # create the 'filtered' bed file 
    FilterArray.create_new_bedfile(old_probe_list)

if __name__ =="__main__":
    main()
