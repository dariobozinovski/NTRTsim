#!/bin/bash

# Copyright © 2012, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
# 
# The NASA Tensegrity Robotics Toolkit (NTRT) v1 platform is licensed
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

# Purpose: Env setup
# Date:    2013-05-04


###############################
# Configuration
local_setup_path="`dirname \"$0\"`"                      # relative
base_dir="`( cd \"$local_setup_path/../../\" && pwd )`"  # absolutized and normalized
install_conf_file="$base_dir/conf/install.conf"
if [ ! -f "$install_conf_file" ]; then
    echo "Missing install.conf ($install_conf_file). Please fix this and try again."
    exit 1
fi
source "$install_conf_file"
###############################

function get_actual_user() {
    who am i | awk '{print $1}'
}

function get_primary_group() {
    id -g -n $1
}

if [ -d "$env_dir" ]; then
    echo "- env directory exists. Ensuring subdirectories."
else
    mkdir "$env_dir"
fi    
pushd "$env_dir" > /dev/null
mkdir bin build downloads include lib 2>/dev/null
popd > /dev/null


# Permissions (change the env dir to be owned by the real current user)
# @todo: do we need to use this? We may not need sudo now...
actual_user=$(get_actual_user)
primary_group=$(get_primary_group $actual_user)
echo "- Changing ownership of env to current user ($actual_user:$primary_group)"
# Test for sudo (try a non-recursive change for speed)
chown $actual_user:$primary_group "$env_dir" 2>/dev/null
if [ ! $? -eq 0 ]; then
  echo "  - ERROR: sudo required -- please re-run the command with sudo."
  exit 1;
fi
# Actually change the permissions
chown -R -P $actual_user:$primary_group "$env_dir"