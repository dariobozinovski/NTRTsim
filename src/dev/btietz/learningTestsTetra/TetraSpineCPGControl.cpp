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

#include "TetraSpineCPGControl.h"

#include <string>


// Should include tgString, but compiler complains since its been
// included from TetraSpineLearningModel. Perhaps we should move things
// to a cpp over there
#include "core/tgLinearString.h"
#include "core/ImpedanceControl.h"

#include "learning/AnnealEvolution/AnnealEvolution.h"
#include "learning/Configuration/configuration.h"

#include "dev/btietz/tgCPGStringControl.h"

/**
 * Defining the adapters here assumes the controller is around and
 * attached for the lifecycle of the learning runs. I.E. that the setup
 * and teardown functions are used for tgModel
 */
TetraSpineCPGControl::TetraSpineCPGControl(BaseSpineCPGControl::Config config,
												std::string args,
                                                std::string ec,
                                                std::string nc) :
BaseSpineCPGControl(config, args, ec, nc)
{    
}

void TetraSpineCPGControl::setupCPGs(BaseSpineModelLearning& subject, array_2D nodeActions, array_4D edgeActions)
{
	std::vector <tgLinearString*> allMuscles = subject.getAllMuscles();
    
    for (std::size_t i = 0; i < allMuscles.size(); i++)
    {
		tgCPGStringControl* pStringControl = new tgCPGStringControl();
        allMuscles[i]->attach(pStringControl);
        m_allControllers.push_back(pStringControl);
    }
    
    /// @todo: redo with for_each
    // First assign node numbers to the info Classes 
    for (std::size_t i = 0; i < m_allControllers.size(); i++)
    {
        m_allControllers[i]->assignNodeNumber(*m_pCPGSys, nodeActions);
    }

    double tension;
    double kPosition;
    double kVelocity;
    double controlLength;
    // Then determine connectivity and setup string
    for (std::size_t i = 0; i < m_allControllers.size(); i++)
    {
        tgCPGStringControl * const pStringInfo = m_allControllers[i];
        assert(pStringInfo != NULL);
        pStringInfo->setConnectivity(m_allControllers, edgeActions);
        
        //String will own this pointer
#if (0) // origninal params
        if (allMuscles[i]->hasTag("outer"))
        {
            tension = 0.0;
            kPosition = 1000.0;
            kVelocity = 100.0;
            controlLength = 17.0;
        }
        else
        {
            tension = 0.0;
            kPosition = 1000.0;
            kVelocity = 100.0;
            controlLength = 15.0 ;
        }
#else // Params for In Won
        if (allMuscles[i]->hasTag("outer"))
        {
            tension = 0.0;
            kPosition = 2000.0;
            kVelocity = 300.0;
            controlLength = 17.5;
        }
        else
        {
            tension = 0.0;
            kPosition = 2000.0;
            kVelocity = 300.0;
            controlLength = 15.0 ;
        }
#endif
        ImpedanceControl* p_ipc = new ImpedanceControl( tension,
                                                        kPosition,
                                                        kVelocity);
        pStringInfo->setupControl(*p_ipc, controlLength);
    }
    
}