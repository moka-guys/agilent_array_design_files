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
        self.OldArrayDesignXML="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\dev\\028469_Guys19_110601_truncated.xml"
        # input xml file for "new" design
        self.NewArrayDesignXML="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\dev\\CGH 4.3_085030_D_F_20170809_Guys19Truncated.xml"
        
        # input bedfile for "new" design
        self.NewArrayDesignBedfile="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\array_design_085030\\CGH 4.3_085030_D_BED_20170809.bed"
        
        # output xml file for "filtered" design
        self.FilteredArrayDesignXML="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\dev\\truncatedtest.xml"
        # output bedfile for "filtered" design
        self.FilteredArrayDesignBedfile="S:\\Genetics_Data2\\Array\\Audits and Projects\\160421 ArrayCGH v4.0 Design\\modified_design_file\\dev\\ignore_me.bed"
        
                
    def get_probe_list(self,XMLInputFile):
        """this function takes a single array design and returns a list of probe names"""
        # an empty list to hold all probes that will be identified when parsing the input design file
        ProbeList=[]
   
        # Using the Element tree module parse the input xml file into python object
        Tree=ET.parse(XMLInputFile)
        
        # set the root of the xml tree so we can use this to loop
        Root=Tree.getroot()
        
        #loop through the file, looking at each 'reporter' section (each reporter section is a probe)
        for Probe in Root.iter('reporter'):
            # add the probe name to the list
            ProbeList.append(Probe.attrib['name'])
        
        print "get_probe_list"
        
        #return list of probes
        return ProbeList
    
    def add_controltype_to_new_probes(self, OldProbeList, FileToFilter):
        """
        This function recieves the list of probes on the 'old' array design and the file path to the 'new' array design
        The 'new' array XML design file is read into a python object and each probe is assessed. If the probe is not present in the 'old' array design it has an attribute of 
        control_type = ignore added to 'turn off' the probe
        The modified XML is then written to the 'filtered' array design file however this does not include non-XML data in the file such as the file type and header   
        """
        
        # load the xml file input to this function into a python object using the element tree package
        Tree=ET.parse(FileToFilter)
        
        # set the root of the file
        Root=Tree.getroot()
        
        # loop through the file, looking at each 'reporter' section (each reporter section is a probe)
        for Probe in Root.iter('reporter'):
            #if the probe name is not in the old array design
            if Probe.attrib['name'] not in OldProbeList:
                # add a flag to ignore the probe
                Probe.attrib['control_type']="ignore"       
                
        # write the modified XML data object to the filtered XML output file.
        Tree.write(self.FilteredArrayDesignXML)
        
                
    def add_non_XML_to_XML_file(self):
        """
        Some non-XML lines are required to be added to the 'filtered' file in order for the design file to be recognised by the scanner.
        These are found at the top of the XML file, before the project tag (usually around 10 lines).
        The top 50 lines of the 'New' array design XML file are read into a list
        The 'filtered' XML file is read back into a list and any lines before the project tag added into this list
        This list is then written back to file
        """
        # open the filtered XML file created above 
        with open(self.FilteredArrayDesignXML,'r') as FilteredXMLFileNoHeader:
            # create a list of all the lines in this file so we can insert lines in as required
            FilteredXMLFileNoHeaderList=FilteredXMLFileNoHeader.readlines()
        
        # open the original array design file to get the non-xml lines 
        with open(self.NewArrayDesignXML,'r') as NewArrayDesignFile:
            # capture the top 50 lines into a list (this should include all the non-XML lines)
            Top50Lines=[next(NewArrayDesignFile) for x in xrange(50)]
        
        
        # capture the first line of the 'filtered' XML file. This can be used to only bring in lines from the 'new' XML design before the XML which has already been captured 
        # take the start of the line (<project) only as the order of the other tags can change
        WhereToStop=str(FilteredXMLFileNoHeaderList[0][0:8])
        
        # loop through the list of lines from the 'new' array design. use enumerate so we can insert the lines into the list at the specific line 
        for Number,Line in enumerate(Top50Lines):
            # set a flag so once we have reached the project tag we can stop
            StopFlag=False
            # when we reach the project tag, change the StopFlag variable to true
            if WhereToStop in Line:
                # set the tag to true so
                StopFlag=True
            # if we haven't reached the xml yet, add the non-xml line into the same place in the filtered xml file list
            elif not StopFlag:
                FilteredXMLFileNoHeaderList.insert(Number,Line)
            # if we have already reached the xml pass
            else:
                pass
        
        # re-write the list with the non-xml added in to file.
        with open(self.FilteredArrayDesignXML,'w') as filtered_file_with_header:
            filtered_file_with_header.writelines(FilteredXMLFileNoHeaderList)
    
    def create_new_bedfile(self, OldProbes):
        """
        This function takes the list of probes on the 'old' array design as an input. 
        It then opens the 'new' array_design bedfile in a list, loops through it assessing if the probe name is on the 'old' array design. 
        If it is the line is written to the 'filtered' bedfile.
        """
        # open the new array design bedfile
        with open(self.NewArrayDesignBedfile,'r') as InputBedfile:
            # put into a list
            BedfileList=InputBedfile.readlines()
        
        # open a new file to write 'filtered' bed file
        with open(self.FilteredArrayDesignBedfile,'w') as FilteredBed:
            # for line in bed file
            for Line in BedfileList:
                # split the bedfile on tab, take the 4th column and remove any new line characters
                ProbeName=Line.split('\t')[3].rstrip()
                # if the probe name is on the old array write to the new bedfile
                if ProbeName in set(OldProbes):
                    FilteredBed.write(Line)
            

def main():
    """
    This function uses the filterarrayDesign class
    """
    #create instance of class
    FilterArray=FilterArrayDesign()
    # Create a list for all probes on the old array design
    OldProbelist=FilterArray.get_probe_list(FilterArray.OldArrayDesignXML) 
    # Create a file containing the probes which have been 'turned off'
    FilterArray.add_controltype_to_new_probes(OldProbelist, FilterArray.NewArrayDesignXML)
    # add in any non-XML lines to the 'filtered' XML file
    FilterArray.add_non_XML_to_XML_file()
    # create the 'filtered' bed file 
    FilterArray.create_new_bedfile(OldProbelist)

if __name__ =="__main__":
    main()

        
