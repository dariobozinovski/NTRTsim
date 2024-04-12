important info for every sim:
-model used: /home/ubuntu/NTRTsim/src/dev/dariostuff/models/isodrop.yaml (iso4ACNC.yaml)
-controller and settings: src/dev/dariostuff/LengthControllerdarYAML.cpp
    double startTime = 2.0;
    double minLength = 0.2;
    double rate = 1;
    double jumpTime = 8;
-data logger interval= 0.01
-nEpisodes 50
-nSteps 10000
-sweep? stiffness 100-i*10 i from 1 to 50