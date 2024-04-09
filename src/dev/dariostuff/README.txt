this is my attempt of using NTRT
Here you will find the most relevant implementation and how to use the simulator(for noobies)

AppisocDarYAML.cpp

there are some feature added respect to other simulations:
-(105-106) choose one of the two line if you want to view the simulaiton or to datalog whithout viewer 
-(119) if the yaml structure is a substructure of the file given in argv[1] manually insert substructure path 
-(127-130) parameters of controller
-(144-172) Data logger, 0 for no data collection, 1 for data collection
-(174-) simulation sweep (nEpisodes = 1 for only one simulation) to change structural properties use function: updateYAMLStiffness( , ) for stiffness, other controllers will be done if neaded
change controller properties look in to lenghtcontroller

YAML files
pretty intuitive to use just create some points in cartesian coordinates and connect them afterwards use builders to assign physical properties

lengthcontroller
added a jumping mechanism: when jumptime reached restlenght resets to initial restlength

-(192)sweep next step function to change values of the controller see example minlenght change