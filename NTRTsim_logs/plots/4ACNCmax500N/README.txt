builders:
  prism_rod:
    parameters:
      restitution: 0.0
      friction: 0.99
      radius: 0.06
      roll_friction: 0.011
      density: 1.7683
    class: tgRodInfo
  springs:
    class: tgBasicActuatorInfo
    parameters:
      stiffness: 300
      pretension: 100
      damping: 10
      max_tension: 70000
  activated_cable:
    parameters:
      damping: 10
      max_tension: 500.0
      stiffness: 10000
      pretension: 0
    class: tgBasicActuatorInfo

    double startTime = 2.0;
    double minLength = 0.1;
    double rate = 0.5;
    double jumpTime = 35;