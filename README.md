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

Graph Database on neo4j:

![Sample Output](https://github.com/rashidahamedmeeran/SDP-Knowledge-extraction-from-drone-manual/blob/main/images/Sample_output.jpg?raw=true)

Terminal output:

![Sample Output](https://github.com/rashidahamedmeeran/SDP-Knowledge-extraction-from-drone-manual/blob/main/images/terminal_output.jpg?raw=true)
