/*
 * Copyright © 2012, United States Government, as represented by the
 * Administrator of the National Aeronautics and Space Administration.
 * All rights reserved.
 *
 * The NASA Tensegrity Robotics Toolkit (NTRT) v1 platform is licensed
 * under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0.
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the License for the specific language
 * governing permissions and limitations under the License.
*/

/**
 * @file AppHorizontalSpine.cpp
 * @brief Contains the definition function main() for App3BarYAML
 * which builds an example 3 bar prism using YAML.
 * @author Andrew Sabelhaus
 * $Id$
 */

// This application
#include "yamlbuilder/TensegrityModel.h"
#include "LengthControllerdarYAMLmanual.h"
// This library
#include "core/terrain/tgBoxGround.h"
#include "core/tgModel.h"
#include "core/tgSimulation.h"
#include "core/tgSimViewGraphics.h"
#include "core/tgWorld.h"
#include "sensors/tgDataLogger2.h"
#include "sensors/tgRodSensorInfo.h"
#include "sensors/tgSpringCableActuatorSensorInfo.h"
#include "sensors/tgCompoundRigidSensorInfo.h"
// Bullet Physics
#include "LinearMath/btVector3.h"
// The C++ Standard Library
#include <iostream>
#include <string>
#include <vector>
#include <yaml-cpp/yaml.h>
#include <cmath>
/**
 * The entry point.
 * @param[in] argc the number of command-line arguments
 * @param[in] argv argv[0] is the executable name
 * @param[in] argv argv[1] is the path of the YAML encoded structure
 * @return 0
 */

void updateYAMLStiffness(const std::string& filename, double newStiffness) {
    try {
        YAML::Node config = YAML::LoadFile(filename);  // Load the current YAML file

        if (config["builders"] && config["builders"]["springs"]) {
            // Assuming the YAML structure has a builders -> springs -> parameters -> stiffness path
            config["builders"]["springs"]["parameters"]["stiffness"] = newStiffness;
        } else {
            throw std::runtime_error("Invalid YAML structure: Expected 'builders/springs/parameters/stiffness' path.");
        }

        // Save the modified YAML file back
        std::ofstream fout(filename);
        fout << config;
    } catch (const YAML::ParserException& ex) {
        std::cerr << "Failed to parse YAML file: " << ex.what() << std::endl;
        throw;
    } catch (const std::exception& ex) {
        std::cerr << "Error: " << ex.what() << std::endl;
        throw;
    }
}

/// @brief 
/// @param argc 
/// @param argv 
/// @return 
int main(int argc, char** argv)
{
    // For this YAML parser app, need to check that an argument path was
    // passed in.
    
    if (argv[1] == NULL)
    {
      throw std::invalid_argument("No arguments passed in to the application. You need to specify which YAML file you wouldd like to build.");
    }
  
    // fill varibles startTime, minLenght, rate, jumpTime trough argv[2], argv[3], argv[4], argv[5]
    // Parse additional command-line arguments
    double rate = 0.1;
    bool datalogger =0;

    // Output parsed variables for confirmation
  
    std::cout << "Rate: " << rate << std::endl;
  
    // create the ground and world. Specify ground rotation in radians
    const double yaw = 0.0;
    const double pitch = 0.0;
    const double roll = 0.0;
    const tgBoxGround::Config groundConfig(btVector3(yaw, pitch, roll));
    // the world will delete this
    tgBoxGround* ground = new tgBoxGround(groundConfig);

    const tgWorld::Config config(98.1); // gravity, dm/sec^2
    tgWorld world(config, ground);

    // create the view
    const double timestep_physics = 0.0001; // seconds
    //const double timestep_physics = 0.001;
    const double timestep_graphics = 1.f/60.f; // seconds

    tgSimViewGraphics view(world, timestep_physics, timestep_graphics);  //visualize one tensegrity
    //tgSimView view(world, timestep_physics, timestep_graphics);        // For running multiple episodes
    // create the simulation
    tgSimulation simulation(view);

    // create the models with their controllers and add the models to the simulation
    // This constructor for TensegrityModel takes the 'debugging' flag as the
    // second argument.
    TensegrityModel* const myModel = new TensegrityModel(argv[1],false);
   
    std::string yamlFilePath = "/home/ubuntu/NTRTsim/src/dev/dariostuff/models/iso4ACNC.yaml";
    
    // Attach a controller to the model, if desired.
    // This is a controller that interacts with a generic TensegrityModel as
    // built by the TensegrityModel file.

    // Parameters for the LengthControllerYAML are specified in that .h file,
    // repeated here:
    // double startTime = 2.0;
    // double minLength = 0.5;
    // double rate = 0.1;
    // double jumpTime = 35;

    std::vector<std::string> tagsToControl;
    // See the threeBarModel.YAML file to see where "vertical_string" is used.
    tagsToControl.push_back("activated_cable");
    
    // Create the controller
     LengthControllerYAMLmanual* const myController = new LengthControllerYAMLmanual(rate,tagsToControl);
    
    // Attach the controller to the model
    
    myModel->attach(myController);
    // Add the model to the world
    simulation.addModel(myModel);
    
    //data logger
    
    if(datalogger){
      // Add sensors using the new sensing framework
      // A string prefix for the filename
      std::string log_filename = "~/NTRTsim/NTRTsim_logs/to_plot/";
    
      // The time interval between sensor readings:
      double timeInterval = 0.005;
      // First, create the data manager
      tgDataLogger2* myDataLogger = new tgDataLogger2(log_filename, timeInterval);
      //std::cout << myDataLogger->toString() << std::endl;
      // Then, add the model to the data logger
      myDataLogger->addSenseable(myModel);
      // Create sensor infos for all the types of sensors that the data logger
      // will create.
      //tgRodSensorInfo* myRodSensorInfo = new tgRodSensorInfo();
      tgSpringCableActuatorSensorInfo* mySCASensorInfo =
        new tgSpringCableActuatorSensorInfo();
      tgCompoundRigidSensorInfo* myCRSensorInfo = new tgCompoundRigidSensorInfo();
      tgRodSensorInfo* myRsensorInfo = new tgRodSensorInfo();
      // Attach the sensor infos to the data logger
      //myDataLogger->addSensorInfo(myRodSensorInfo);
      myDataLogger->addSensorInfo(mySCASensorInfo);
      myDataLogger->addSensorInfo(myCRSensorInfo);
      myDataLogger->addSensorInfo(myRsensorInfo);
      // Next, attach it to the simulation
      simulation.addDataManager(myDataLogger);
      }

    int nEpisodes = 1; // Number of episodes ("trial runs")
    int nSteps = 30/timestep_physics;; // Number of steps in each episode, 60k is 100 seconds (timestep_physics*nSteps)
    for (int i=0; i<nEpisodes; i++) {
      simulation.run(nSteps);
      std::cout << "Episode " << (i+1 ) << " completed."<< std::endl;
      simulation.reset();
      }
    
    // teardown is handled by delete
    return 0;
}

//provare altre forme -non credo che faro
//fare README per le analisi -fatto
//salvare tutto su git -fatto
//salvare simulazioni su git -fatto
//trovare l'errore nelle simulazioni con dati realistici forse la alta tensione porta a microvibrazioni che spostano il corpo -ora funziona non so perche cambiato hardware
//colorare le molle o numerarle nella simulazione per identificarle
//riominciare da capo con modello semplice:
//centrl actuated 3 A fare analisi e farla bene e analizzare i dati capire percentuale di energia in salto e quanta invece persa 
// abbasasre rate di compressione e creare grafico di tensione attuatore per vedere come si distribuisce lo stress durante la copressione
//