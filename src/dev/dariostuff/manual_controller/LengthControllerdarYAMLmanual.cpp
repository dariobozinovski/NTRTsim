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
 * @file LengthControllerYAML.cpp
 * @brief Implementation of LengthControllerYAML.
 * @author Drew Sabelhaus
 * $Id$
 */

// This module
#include "LengthControllerdarYAMLmanual.h"  
// This application
#include "yamlbuilder/TensegrityModel.h"
// This library
#include "core/tgBasicActuator.h"
#include "core/tgSpringCableActuator.h"
#include "core/tgString.h"
#include "core/tgTags.h"

//#include "sensors/tgDataObserver.h"
// The C++ Standard Library
#include <cassert>
#include <stdexcept>
#include <vector>
#include <iostream>
#include "helpers/FileHelpers.h"
#include <stdexcept>

// Constructor assigns variables, does some simple sanity checks.
// Also, initializes the accumulator variable timePassed so that it can
// be incremented in onStep.
LengthControllerYAMLmanual::LengthControllerYAMLmanual(double rate,
					   std::vector<std::string> tagsToControl):
  m_rate(rate),
  m_tagsToControl(tagsToControl)
 
{
  // rate must be greater than zero
  if( rate < 0.0 ) {
    throw std::invalid_argument("Rate cannot be negative.");
  }
  
  // @TODO: what checks to make on tags?
}

/**
 * The initializeActuators method is call in onSetup to put pointers to 
 * specific actuators in the cablesWithTags array, as well as store the initial
 * rest lengths in the initialRL map.
 */
void LengthControllerYAMLmanual::initializeActuators(TensegrityModel& subject,
					       std::string tag) {
  //DEBUGGING
  std::cout << "Finding cables with the tag: " << tag << std::endl;
  // Pick out the actuators with the specified tag
  std::vector<tgBasicActuator*> foundActuators = subject.find<tgBasicActuator>(tag);
  std::cout << "The following cables were found and will be controlled: "
	    << std::endl;
  //Iterate through array and output strings to command line
  for (std::size_t i = 0; i < foundActuators.size(); i ++) {	
    std::cout << foundActuators[i]->getTags() << std::endl;
    // Also, add the rest length of the actuator at this time
    // to the list of all initial rest lengths.
    initialRL[foundActuators[i]->getTags()] = foundActuators[i]->getRestLength();
    //DEBUGGING:
    std::cout << "Cable rest length at t=0 is "
	      << initialRL[foundActuators[i]->getTags()] << std::endl;
    //DEBUG minlengthchange
    //std::cout << "target restlength:" <<m_minLength<< std::endl; 
  }
  // Add this list of actuators to the full list. Thanks to:
  // http://stackoverflow.com/questions/201718/concatenating-two-stdvectors
  cablesWithTags.insert( cablesWithTags.end(), foundActuators.begin(),
			 foundActuators.end() );
}

/**
 * For this controller, the onSetup method initializes the actuators,
 * which means just store pointers to them and record their rest lengths.
 * This method calls the helper initializeActuators.
 */
void LengthControllerYAMLmanual::onSetup(TensegrityModel& subject)
{
  
  std::cout << "Setting up the LengthControllerYAML controller." << std::endl;
  //	    << "Finding cables with tags: " << m_tagsToControl
  //	    << std::endl;
  cablesWithTags = {};
  // For all the strings in the list, call initializeActuators.
  std::vector<std::string>::iterator it;
  for( it = m_tagsToControl.begin(); it < m_tagsToControl.end(); it++ ) {
    // Call the helper for this tag.
    initializeActuators(subject, *it);
  }
  //set all FinalRestLengths to initialRL
  for (auto& cable : cablesWithTags) {
    finalRestLength[cable] = initialRL[cable->getTags()];
  }
  
  std::cout << "Finished setting up the controller." << std::endl;    
}


void LengthControllerYAMLmanual::onStep(TensegrityModel& subject, double dt)
{
    int print=0;
    for (auto& cable : cablesWithTags) {
        double currRestLength = cable->getRestLength();
        double targetLength = finalRestLength[cable];
        
        if (fabs(currRestLength - targetLength) > 0.01) { // Using a small threshold to determine 'different'
            double nextRestLength = currRestLength + (targetLength > currRestLength ? m_rate * dt : -m_rate * dt);
            // Clamping to ensure we do not overshoot the target
            if (m_rate * dt > fabs(currRestLength - targetLength)) {
                nextRestLength = targetLength;
            }
            //cout cable final and current rest length but for only first cable
            
            std::cout << "Cable: " << cable->getTags()<< " Current Rest Length: " << currRestLength << " Target Rest Length: " << targetLength << std::endl;
            
            cable->setControlInput(nextRestLength, dt);
        }
    print++;
    }
    handleConsoleInput(dt);

}
  
  void LengthControllerYAMLmanual::setNonBlockingInput() {
    struct termios settings;
    tcgetattr(STDIN_FILENO, &settings);
    settings.c_lflag &= ~(ICANON | ECHO); // Disable canonical mode and echo
    tcsetattr(STDIN_FILENO, TCSANOW, &settings);
}

void LengthControllerYAMLmanual::restoreInput() {
    struct termios settings;
    tcgetattr(STDIN_FILENO, &settings);
    settings.c_lflag |= (ICANON | ECHO); // Enable canonical mode and echo
    tcsetattr(STDIN_FILENO, TCSANOW, &settings);
}

void LengthControllerYAMLmanual::handleConsoleInput(double dt)
{
    setNonBlockingInput();

    fd_set read_fds;
    FD_ZERO(&read_fds);
    FD_SET(STDIN_FILENO, &read_fds);

    struct timeval timeout;
    timeout.tv_sec = 0; // No waiting
    timeout.tv_usec = 0;

    // Check if there's input to read
    if (select(STDIN_FILENO + 1, &read_fds, NULL, NULL, &timeout) == 1) {
        std::string input;
        std::getline(std::cin, input); // Use getline to read the whole line

        if (!input.empty()) {
            if (input == "j") {
                resetAllActuatorsToInitial(dt);
                restoreInput();
                return;
            }

            std::istringstream iss(input);
            int cableIndex;
            double newLengthPercent;

            iss >> cableIndex;
            iss >> newLengthPercent;

            if (!iss.fail() && newLengthPercent >= 0 && newLengthPercent <= 1) {
                if (cableIndex == 0) {
                    for (auto& cable : cablesWithTags) {
                        double initialLength = initialRL[cable->getTags()];
                        finalRestLength[cable] = initialLength * newLengthPercent;
                    }
                } else if (cableIndex > 0 && cableIndex <= (int)cablesWithTags.size()) {
                    tgBasicActuator* selectedCable = cablesWithTags[cableIndex - 1];
                    double initialLength = initialRL[selectedCable->getTags()];
                    finalRestLength[selectedCable] = initialLength * newLengthPercent;
                }
            } else {
                std::cerr << "Invalid input or out of range values" << std::endl;
            }
        }
    }
}
// void LengthControllerYAMLmanual::handleConsoleInput(double dt)
// {
//     std::string input;
//     if (std::getline(std::cin, input)) {
//         std::istringstream iss(input);
//         int cableIndex;
//         double newLengthPercent;

//         iss >> cableIndex;
//         if (iss.fail()) {
//             std::cerr << "Invalid input" << std::endl;
//             return;
//         }

//         if (cableIndex == 'j') {
//             resetAllActuatorsToInitial(dt);
//             return;
//         }

//         iss >> newLengthPercent;
//         if (newLengthPercent < 0 || newLengthPercent > 1) {
//             std::cerr << "Length percentage must be between 0 and 1." << std::endl;
//             return;
//         }

//         // Adjust all cables if index is 0
//         if (cableIndex == 0) {
//             for (auto& cable : cablesWithTags) {
//                 double initialLength = initialRL[cable->getTags()];
//                 finalRestLength[cable] = initialLength * newLengthPercent;

//             }
//         } else if (cableIndex > 0 && cableIndex <= (int)cablesWithTags.size()) {
//             // Adjust specified cable
//             tgBasicActuator* selectedCable = cablesWithTags[cableIndex - 1];
//             double initialLength = initialRL[selectedCable->getTags()];
//             finalRestLength[selectedCable] = initialLength * newLengthPercent;
//         } else {
//             std::cerr << "Cable index out of range" << std::endl;
//         }
//     }
// }

void LengthControllerYAMLmanual::resetAllActuatorsToInitial(double dt)
{
    for (auto& cable : cablesWithTags) {
        finalRestLength[cable]=initialRL[cable->getTags()];
        //for 100 time steps, set the rest length to the initial rest length
        for(int i=0; i<1000; i++){
          cable->setControlInput(initialRL[cable->getTags()], dt);
          //  DEBUGGING
          // std::cout << "Cable: " << cable->getTags()<< " Current Rest Length: " << cable->getRestLength() << " Target Rest Length: " << finalRestLength[cable] << std::endl;

        }
               
    }
}

 
