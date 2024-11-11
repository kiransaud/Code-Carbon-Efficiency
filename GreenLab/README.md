# GreenLab

# Experiment Replication Package

This README provides detailed instructions for setting up and running the experiment replication package. The package is designed to evaluate the accuracy of energy consumption estimates provided by CodeCarbon under various operational settings.

### Prerequisites

Before you begin, make sure you have Python installed on your system. This guide assumes you are using Python 3.

### Setup Instructions

Follow these steps to set up your environment and run the experiments:

### Step 1: Install Python3-tk

sudo apt-get install python3-tk


### Install virtualenv if it is not installed
pip3 install virtualenv

### Create a virtual environment in the current directory
virtualenv venv

### Activate the virtual environment
On macOS and Linux
source venv/bin/activate


pip install -r requirements.txt

python3 experiment-runner/code_carbon_accuracy_measurement/RunnerConfig-921f0e68-8c73-11ef-8a74-e6df4daffa1e.py

deactivate

