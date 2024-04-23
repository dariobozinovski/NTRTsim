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
#include "LengthControllerdarYAML.h"
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
LengthControllerYAML::LengthControllerYAML(double startTime,
					   double minLength,
					   double rate,
             double jumpTime,
					   std::vector<std::string> tagsToControl) :
  m_startTime(startTime),
  m_jumpTime(jumpTime),
  m_minLength(minLength),
  m_rate(rate),
  m_tagsToControl(tagsToControl),
  m_timePassed(0.0),
  
  Ijumped(0)
  
{
  // start time must be greater than or equal to zero
  if( m_startTime < 0.0 ) {
    throw std::invalid_argument("Start time must be greater than or equal to zero.");
  }
  // min length must be between 1 and 0
  else if( m_minLength > 1 ) {
    throw std::invalid_argument("minLength is a percent, must be less than 1. (100%)");
  }
  else if( m_minLength < 0.0) {
    throw std::invalid_argument("minLength is a percent, must be greater than 0.");
  }
  // rate must be greater than zero
  else if( rate < 0.0 ) {
    throw std::invalid_argument("Rate cannot be negative.");
  }
  if( m_jumpTime < m_startTime &&m_jumpTime==0) {
    throw std::invalid_argument("Jump time must be greater than start Time or 0 for no jump");
  }
  // @TODO: what checks to make on tags?
}



/**
 * The initializeActuators method is call in onSetup to put pointers to 
 * specific actuators in the cablesWithTags array, as well as store the initial
 * rest lengths in the initialRL map.
 */
void LengthControllerYAML::initializeActuators(TensegrityModel& subject,
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
void LengthControllerYAML::onSetup(TensegrityModel& subject)
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
  std::cout << "Finished setting up the controller." << std::endl;    
}

void LengthControllerYAMLmanual::handleConsoleInput(double dt)
{
    setNonBlockingInput();

    char input[256]; // Buffer to hold input
    if (read(STDIN_FILENO, input, 255) > 0) {
        input[255] = '\0'; // Ensure null termination

        std::istringstream iss(input);
        int cableIndex;
        double newLengthPercent;

        iss >> cableIndex;
        if (iss.fail()) {
            std::cerr << "Invalid input" << std::endl;
            restoreInput();
            return;
        }

        if (input[0] == 'j') { // Checking the first character for 'j'
            resetAllActuatorsToInitial(dt);
            restoreInput();
            return;
        }

        iss >> newLengthPercent;
        if (newLengthPercent < 0 || newLengthPercent > 1) {
            std::cerr << "Length percentage must be between 0 and 1." << std::endl;
            restoreInput();
            return;
        }

        // Adjust all cables if index is 0
        if (cableIndex == 0) {
            for (auto& cable : cablesWithTags) {
                double initialLength = initialRL[cable->getTags()];
                finalRestLength[cable] = initialLength * newLengthPercent;
            }
        } else if (cableIndex > 0 && cableIndex <= (int)cablesWithTags.size()) {
            // Adjust specified cable
            tgBasicActuator* selectedCable = cablesWithTags[cableIndex - 1];
            double initialLength = initialRL[selectedCable->getTags()];
            finalRestLength[selectedCable] = initialLength * newLengthPercent;
        } else {
            std::cerr << "Cable index out of range" << std::endl;
        }
    }

    restoreInput(); // Restore terminal settings after input handling
}
void LengthControllerYAML::reset() {
    m_timePassed = 0.0;
    Ijumped = 0;
    
    // Optionally, reinitialize other necessary components
}
void LengthControllerYAML::nextStep() {
  //insrt values to sweep
  reset();

  //change minLength
  //m_minLength=m_minLength-0.1;


}
 
