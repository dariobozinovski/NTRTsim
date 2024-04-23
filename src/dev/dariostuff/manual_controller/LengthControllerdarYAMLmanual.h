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

#ifndef HORIZONTAL_SPINE_CONTROLLER_H
#define HORIZONTAL_SPINE_CONTROLLER_H

/**
 * @file HorizontalSpineController.h
 * @brief Contains the definition of class LengthControllerYAML
 * @author Drew Sabelhaus
 * $Id$
 */

// The NTRT core library
#include "core/tgObserver.h"
#include "core/tgSubject.h"
#include "core/tgTags.h"

// The C++ standard library
#include <string>
#include <vector>
#include <map>
#include <termios.h>
#include <unistd.h>
#include <iostream>
#include <sstream>

// Forward declarations
class TensegrityModel;
class tgBasicActuator;

/**
 * A controller to apply the length change to cables in a icosahedronal TensegrityModel with console inputs
 */
class LengthControllerYAMLmanual : public tgObserver<TensegrityModel>, public tgSubject<LengthControllerYAMLmanual>
{
public:
	
  /**
   * Construct a HorizontalSpineController.
   * @param[in] rate, the rate at which the rest length of the cables will be
   * changed. Expressed in meters/sec.
   
   * @param[in] tagsToControl, a vector (array) of strings, which is a list of the 
   * tags of all the
   * cables upon which to act. All the cables which have a tag in this list of tags
   * will be acted upon by this controller.
   */
  LengthControllerYAMLmanual(double rate,std::vector<std::string> tagsToControl);
    
  /**
   * Nothing to delete, destructor must be virtual
   */
  virtual ~LengthControllerYAMLmanual() { }

  /**
   * Apply the controller. On setup, adjust the cable
   * lengths one time.
   * @param[in] subject - the TensegrityModel that is being controlled. Must
   * have a list of allMuscles populated
   */
  virtual void onSetup(TensegrityModel& subject);
    
  /**
   * Changes the cables' lengths at some specified timestep.
   * @param[in] subject - the TensegrityModel that is being controlled. Must
   * have a list of allMuscles populated
   * @param[in] dt, current timestep must be positive
   */
  virtual void onStep(TensegrityModel& subject, double dt);

  void handleConsoleInput(double dt);
  
  void resetAllActuatorsToInitial(double dt);
  void restoreInput();
  void setNonBlockingInput();
protected:

  /**
   * A helper function to find and initialize the actuators that this class
   * will control.
   * @param[in] tag, a string of the tag for which to search in the list of 
   * actuators in this model.
   */
  void initializeActuators(TensegrityModel& subject, std::string tag);
    
private:
	
  /**
   * The private variables for each of the values passed in to the constructor.
   */
  
  double m_rate; // Rate of change of rest length
  std::vector<std::string> m_tagsToControl;
  
  /**
   * Need an accumulator variable to determine when to start the controller.
   */

  /**
   * The start length of each of the cables must be recorded.
   * This map takes a string (the space-separated list of all the tags for
   * an individual cable) and outputs a double (the rest length at time t=0.)
   */
  typedef std::map<tgTags, double> InitialRestLengths;
  InitialRestLengths initialRL;
  std::map<tgBasicActuator*, double> finalRestLength;  // Target rest lengths for actuators

  /**
   * A list of all the actuators to control. This is populated in onSetup
   * by using m_tagsToControl.
   */
  std::vector<tgBasicActuator*> cablesWithTags;
   
};

#endif // HORIZONTAL_SPINE_CONTROLLER_H
