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


git

to submittare changes to branch
git status
git add .
git status
git commit -m "a message"
git push fork nome name-of-branch

to create new branch

git checkout -b name-branch




to do:
/provare altre forme -non credo che faro
//fare README per le analisi -fatto
//salvare tutto su git -fatto
//salvare simulazioni su git -fatto
//trovare l'errore nelle simulazioni con dati realistici forse la alta tensione porta a microvibrazioni che spostano il corpo -ora funziona non so perche cambiato hardware
//riominciare da capo con modello semplice:
//centrl actuated 3 A fare analisi e farla bene e analizzare i dati capire percentuale di energia in salto e quanta invece persa 
// abbasasre rate di compressione e creare grafico di tensione attuatore per vedere come si distribuisce lo stress durante la copressione
//different approaches to directional jumping form full compressed state (late realese, less compression)

//directional jumping is more complicated that it seams
//approach make struts longer then nodes to avoid rods going under other rods


//fallingn simulatiom
//pretension does it change that muchg
//spring non linearity 




//colorare le molle o numerarle nella simulazione per identificarle
convertire tutto per fare simulazionio piu facilmente
plottare elongation a forza
aggiungere massa e vedere se e possibile 
//creare palla in mezzo e attuatore veso la palla perche la simulazione non ha senso collassa in modo strano
fare prototipo di attuatore a 3 nodi
succede qualcosa quando le molle sono a restlenght