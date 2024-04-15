builders:
  activated_cable:
    class: tgBasicActuatorInfo
    parameters:
      stiffness: 200000
      max_tension: 500.0
      damping: 0.01
      pretension: 0
  prism_rod:
    parameters:
      restitution: 0.0
      friction: 0.5
      density: 1.7683
      radius: 0.06
      roll_friction: 0.001
    class: tgRodInfo
  springs:
    class: tgBasicActuatorInfo
    parameters:
      max_tension: 70000
      stiffness: 400
      pretension: 100
      damping: 1


double startTime = 2.0;
    double minLength = 0.557;
    double rate = 0.1;
    double jumpTime = 35;

iso3A

complete collapse of structure in 2d