
builders:
  activated_cable:
    parameters:
      max_tension: 500.0
      pretension: 0
      damping: 0.01
      stiffness: 200000
    class: tgBasicActuatorInfo
  prism_rod:
    class: tgRodInfo
    parameters:
      roll_friction: 0.001
      friction: 0.5
      restitution: 0.0
      density: 1.7683
      radius: 0.06
  extensions:
    parameters:
      friction: 0.5
      density: 0.001
      roll_friction: 0.001
      restitution: 0.0
      radius: 0.06
    class: tgRodInfo
  sphere:
    parameters:
      radius: 0.0
      density: 0.003
      friction: 1
    class: tgSphereInfo
  springs:
    class: tgBasicActuatorInfo
    parameters:
      stiffness: 200
      pretension: 100
      max_tension: 70000
      damping: 1

double startTime = 2;
    double minLength = 0.55;
    double rate = 0.2;
    double jumpTime = 17;
    bool datalogger = 1;
from 200 to 580
#!/bin/bash
cd /home/ubuntu/NTRTsim/build/dev/dariostuff/streight_jump
./AppisocDarYAML /home/ubuntu/NTRTsim/src/dev/dariostuff/models/isodrop3Aext.yaml 2.0 0.55 0.2 17 1 40 200 10

