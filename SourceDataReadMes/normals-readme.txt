This documentation describes the record format for the normals files on 
/pub/data/cirs/climdiv that have the filenames:

climdiv-norm-cddcdv-vx.y.z-YYYYMMDD
climdiv-norm-hddcdv-vx.y.z-YYYYMMDD
climdiv-norm-pcpndv-vx.y.z-YYYYMMDD
climdiv-norm-tmaxdv-vx.y.z-YYYYMMDD
climdiv-norm-tmindv-vx.y.z-YYYYMMDD
climdiv-norm-tmpcdv-vx.y.z-YYYYMMDD

climdiv-norm-cddcst-vx.y.z-YYYYMMDD
climdiv-norm-hddcst-vx.y.z-YYYYMMDD
climdiv-norm-pcpnst-vx.y.z-YYYYMMDD
climdiv-norm-tmaxst-vx.y.z-YYYYMMDD
climdiv-norm-tminst-vx.y.z-YYYYMMDD
climdiv-norm-tmpcst-vx.y.z-YYYYMMDD


                                    nClimDiv
                           DIVISIONAL AND STATEWIDE
                       NORMALS VALUES FOR SPECIAL PERIODS

                                    MAY 2015

*While these long-term averages are not official normals as published by the
NCEI Normals Program, they can be used in a similar way to normals when using
nClimDiv data. They are referred to as "normals" for convenience throughout
this document.

Parameters for which mean monthly normals values are generated include:

Maximum Temperature
Minimum Temperature
Mean Temperature
Precipitation
Heating Degree Days
Cooling Degree Days

In these files, monthly maximum, minimum and mean temperature (deg. F. to 
10ths, national temperature to 100ths), precipitation (inches to 100ths), 
and degree days (to the nearest whole degree) are computed for the 
following periods:

1901-1930  30-year periods in intervals of 10 years
1911-1940
1921-1950
1931-1960
1941-1970
1951-1980
1961-1990
1971-2000
1981-2010
1991-2020

1901-2000 20th century
1895-2020 long term average

    ** Please see the file format explanation below for information
         on how to decipher these periods in the data files **


These files are updated on a monthly basis and are simple arithmetic averages
of monthly data values for months during the specified years.  Monthly CDD and
HDD normals are not computed for Alaska since the degree day algorithm does not
work well for Alaska's climate. 

STATE CODE TABLE: 

         Range of values for the divisions is 01-91.

             01 Alabama                 28 New Jersey
             02 Arizona                 29 New Mexico
             03 Arkansas                30 New York
             04 California              31 North Carolina
             05 Colorado                32 North Dakota
             06 Connecticut             33 Ohio
             07 Delaware                34 Oklahoma
             08 Florida                 35 Oregon
             09 Georgia                 36 Pennsylvania
             10 Idaho                   37 Rhode Island
             11 Illinois                38 South Carolina
             12 Indiana                 39 South Dakota
             13 Iowa                    40 Tennessee
             14 Kansas                  41 Texas
             15 Kentucky                42 Utah
             16 Louisiana               43 Vermont
             17 Maine                   44 Virginia
             18 Maryland                45 Washington
             19 Massachusetts           46 West Virginia
             20 Michigan                47 Wisconsin
             21 Minnesota               48 Wyoming
             22 Mississippi             50 Alaska
             23 Missouri   
             24 Montana   
             25 Nebraska 
             26 Nevada  
             27 New Hampshire

    Range of values for the states, regions and nation is 001-110.

          001 Alabama         030 New York
          002 Arizona         031 North Carolina
          003 Arkansas        032 North Dakota
          004 California      033 Ohio
          005 Colorado        034 Oklahoma
          006 Connecticut     035 Oregon
          007 Delaware        036 Pennsylvania
          008 Florida         037 Rhode Island
          009 Georgia         038 South Carolina
          010 Idaho           039 South Dakota
          011 Illinois        040 Tennessee
          012 Indiana         041 Texas
          013 Iowa            042 Utah
          014 Kansas          043 Vermont
          015 Kentucky        044 Virginia
          016 Louisiana       045 Washington
          017 Maine           046 West Virginia
          018 Maryland        047 Wisconsin
          019 Massachusetts   048 Wyoming
          020 Michigan        050 Alaska     
          021 Minnesota       101 Northeast Region 
          022 Mississippi     102 East North Central Region  
          023 Missouri        103 Central Region  
          024 Montana         104 Southeast Region  
          025 Nebraska        105 West North Central Region  
          026 Nevada          106 South Region  
          027 New Hampshire   107 Southwest Region  
          028 New Jersey      108 Northwest Region  
          029 New Mexico      109 West Region
                              110 National (contiguous 48 States) 

DIVISIONAL FILE FORMAT:

Element          Record
Name             Position    Element Description

STATE-CODE          1-2      STATE-CODE as indicated in State Code Table 
                             above.  Range of values is 01-91.

DIVISION-NUMBER     3-4      DIVISION NUMBER - Range of values 01-13.



STATE/REGIONAL/NATIONAL FILE FORMAT:

STATE-CODE          1-3      STATE-CODE as indicated in State Code Table 
                             above. Range of values is 001-110 for standard
		             states, regions and national, 111-465 for special
                             regions.

DIVISION-NUMBER     4        DIVISION NUMBER - Value is 0 which indicates an
                             area-averaged element.



REMAINING FILE FORMAT FOR DIVISIONAL/STATE/REGIONAL/NATIONAL:

ELEMENT CODE        5-6      01 = Precipitation
                             02 = Average Temperature
                             25 = Heating Degree Days
                             26 = Cooling Degree Days
                             27 = Maximum Temperature
                             28 = Minimum Temperature

YEAR                7-10     This is the code used to identify special 
			     normals periods.

				YEAR  MEANING
				----  -------
				0001  means 1901-1930
				0002  means 1911-1940
				0003  means 1921-1950
				0004  means 1931-1960
				0005  means 1941-1970
				0006  means 1951-1980
				0007  means 1961-1990
				0008  means 1971-2000
				0009  means 1981-2010
				0010  means 1991-2020
				0031  means 1901-2000
				0032  means 1895-2020

(all data values are right justified):

JAN-VALUE          11-17     Monthly Temperature format (f7.2)
                             Range of values -50.00 to 140.00 degrees Fahrenheit.
                             Decimals retain a position in the 7-character
                             field.  Missing values in the latest year are
                             indicated by -99.90.

                             Monthly Precipitation format (f7.2)
                             Range of values 00.00 to 99.99.  Decimal point
                             retains a position in the 7-character field.
                             Missing values in the latest year are indicated
                             by -9.99.

                             Monthly Degree Day format (f7.0)
                             Range of values 0000. to 9999.  Decimal point
                             retains a position in the 7-character field.
                             Missing values in the latest year are indicated
                             by -9999..

FEB-VALUE          18-24     

MAR-VALUE          25-31    

APR-VALUE          32-38   

MAY-VALUE          39-45  

JUNE-VALUE         46-52     

JULY-VALUE         53-59     

AUG-VALUE          60-66     

SEPT-VALUE         67-73     

OCT-VALUE          74-80     

NOV-VALUE          81-87     

DEC-VALUE          88-94     
