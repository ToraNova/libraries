#!/bin/bash

# SOURCE THIS SCRIPT TO LOAD THE LIBRARY PATH

export LD_LIBRARY_PATH=$(pwd)
env | grep LD_LIBRARY_PATH
