#!/usr/bin/env bash

# Arguments
STOP_TYPE=$1

export JAVA_HOME=/home/vcap/app/.java-buildpack/open_jdk_jre
export PATH=$PATH:$JAVA_HOME/bin
echo $JAVA_HOME

source /home/vcap/app/.profile.d/startup.sh
${STOP_TYPE}.sh