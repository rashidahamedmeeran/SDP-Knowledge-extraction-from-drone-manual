This program allows the user to extract features from the drone manual automatically and store them as a graph database in neo4j

**Features being extracted:**
  - Dimensions
  - Weight
  - Payload
  - Limitaions
  - Emergency Procedures

**Instructions on usage:**
  - GIVEN that you have the code(SDP_code.py) and all the drone manuals in the same folder
  - AND You enter the manual names under the variable 'files' in the form of list
  - AND You enter the correct URL and authentication details for the neo4j graph database under the variable 'driver'
  - When you run the program using the command line 'python3 SDP_code.py'
  - THEN you get the output(extracted features) printed and also formed as a neo4j graph database

**Sample drone manuals added:**
  - Freefly ALTA 8 Specifications - Dimensions, Weight & Payload.pdf
  - alta-8-pro-manual.pdf
  - Matrice_600_User_Manual_v1_EN_1208.pdf
  - anafi_user_guide_v6.7.0.1.pdf
  - Elios 2 - Brochure EN LW.pdf
  
**Sample Output for 5 Drone manuals:**

  **Graph Database on neo4j:**

![Sample Output](https://github.com/rashidahamedmeeran/SDP-Knowledge-extraction-from-drone-manual/blob/main/images/Sample_output.jpg?raw=true)

  **Terminal output:**
'''
================================================================
Freefly ALTA 8 Specifications - Dimensions, Weight & Payload.pdf
================================================================


----------
Dimensions:
----------
        unfolded diameter: 1325 mm
        folded diameter: 660 mm
        height: 263 mm


------
Weight:
------
        6.2 kg


-------
Payload:
-------
        not specified


-----------
Limitations:
-----------
        note these limitations are advisory in nature and do not extend or restrict limitations provided by governing aviation authorities.
        warning always refer to the following aircraft limitations section for complete information on allowable maximum gross weights at different altitudes and temperatures before any ﬂight.
        powerplant limitations maximum rpm6300 RPM
        environmental limitations do not ﬂy alta 8 in temperatures exceeding 45°c (113°f) or below -20°c(-4°f).5


--------------------
Emergency procedures:
--------------------
        not specified


=====================
alta-8-pro-manual.pdf
=====================


----------
Dimensions:
----------
        unfolded diameter: 1325 mm
        folded diameter: 660 mm
        unfolded height: 263 mm


------
Weight:
------
        6.2 kg


-------
Payload:
-------
        9.1 kg


-----------
Limitations:
-----------
        limitations limitations these limitations are advisory in nature and do not extend or restrict limitations provided by governing aviation authorities.
        environmental limitations do not fly alta pro in temperatures exceeding 45ºc (113ºf) or below -20ºc(-4ºf).


--------------------
Emergency procedures:
--------------------
        emergency procedures emergency guidance the emergency procedures listed in this section are the recommended practices for handling the aircraft in the event of an aircraft emergency. this guidance should be considered and applied as necessary. the risk of an emergency can be reduced substantially through proper aircraft maintenance, by performing thorough inspections before and after all flights, and with careful pre-flight planning. emergency situations are dynamic events, and not all conditions or procedures can be anticipated or applied during the event. these procedures are not a substitute for a thorough understanding of aircraft systems and sound pilot judgment. in general, if an emergency occurs, three basic actions can be applied to most situations:1. maintain aircraft control—small emergencies can quickly escalate if the pilot is distracted attempting to troubleshoot the problem. always maintain visual contact with the aircraft during an emergency to reduce the likelihood of losing orientation. 2. analyze the situation—once the aircraft is stabilized, begin to assess the cause of the emergency if practical. 3. take appropriate action—in many cases, the appropriate action will be to land the aircraft as soon as possible. always consider the safety of yourself and others before attempting to save the aircraft in an emergency.


======================================
Matrice_600_User_Manual_v1_EN_1208.pdf
======================================


----------
Dimensions:
----------
        dimensions: 505 mm
        unfolded dimensions: 640 mm
        width: 170 mm


------
Weight:
------
        15.1 kg


-------
Payload:
-------
        5.5 kg


-----------
Limitations:
-----------
        not specified


--------------------
Emergency procedures:
--------------------
        not specified


=============================
anafi_user_guide_v6.7.0.1.pdf
=============================


----------
Dimensions:
----------
        folded : 94x152x72mm
        unfolded : 153x152x116mm


------
Weight:
------
        386g


-------
Payload:
-------
        not specified


-----------
Limitations:
-----------
        not specified


--------------------
Emergency procedures:
--------------------
        not specified


============================
Elios 2 - Brochure EN LW.pdf
============================


----------
Dimensions:
----------
        dimension: 40 cm
        dimensions: 61 x 44 x 53 cm


------
Weight:
------
        11.5 kg


-------
Payload:
-------
        1450 g


-----------
Limitations:
-----------
        not specified


--------------------
Emergency procedures:
--------------------
        not specified
'''
![Sample Output](https://github.com/rashidahamedmeeran/SDP-Knowledge-extraction-from-drone-manual/blob/main/images/terminal_output.jpg?raw=true)
