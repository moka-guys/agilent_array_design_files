# agilent_array_design_files
This repository contains scripts used to search and manipulate agilent array design files

## turn_probes_off.py
When probes are added to an array design, these need to be validated and the resulting validation doc needs to be submitted to UKAS as an ISO15189 extension to scope. To speed things up, the new array design can be ordered, used and reported with a UKAS logo on the report (i.e. as an accredited service) if the new probes are excluded from analysis.

Probes can be 'turned off' by setting that probe as a control probe in the design XML file, a file which details all the probes on the design and how they should be interpreted by the array analysis software and algorithms.

This script takes the 'old' accredited array design and the 'new' unaccredited array design and creates a 'filtered' design XML file based on the 'new' array design, but with any unaccredited probes (not present on the 'old' array) 'turned off'.

This 'filtered' array must be validated against the 'old' array which enables the 'new' array slides to be used whilst ensuring the test is ISO accredited (until the full 'new' array design goes through extension to scope).

This script also creates a 'filtered' bed file, based on the 'new' array design bed file, but with any probes not on the 'old' array design removed.
