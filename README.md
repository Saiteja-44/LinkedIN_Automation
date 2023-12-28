# LinkedIn Automation Tool

This project is an automation tool built using Python and Selenium for performing actions on LinkedIn, such as sending connection requests and personalized messages based on user-defined inputs.

## Overview

The LinkedIn Automation Tool consists of two main Python scripts:

1. **linkedin.py**: Contains the automation code utilizing the Selenium WebDriver to perform various actions on the LinkedIn website.
2. **gui.py**: A graphical user interface script designed to interact with `linkedin.py` by collecting user inputs and passing them as arguments for the automation process.

## Requirements

- Python 3.x
- Selenium WebDriver
- Chrome WebDriver (chromedriver.exe)
- Tkinter (for GUI interface)

## Installation

1. **Clone the repository:**

   ```
   git clone https://github.com/your-username/linkedin-automation.git
   cd linkedin-automation
   ```

## Install dependencies:

Ensure Python 3.x is installed. Install required Python packages using pip:

    pip install -r requirements.txt

Download Chrome WebDriver:
Download the appropriate Chrome WebDriver from Chromedriver Downloads and place chromedriver.exe in the project directory.

## Usage

Run the graphical interface:

Execute the following command in the terminal:

    python gui.py

Fill in the required details in the GUI:

Enter your LinkedIn username and password.
Provide the search term, company name, number of pages, and a personalized message.
Click on the "Submit" or "Run Automation" button.

Observe the automation process:

The linkedin.py script will be executed with the provided inputs, automating actions on the LinkedIn website.
The console may display progress or status messages during execution.

## Important Note

Ensure that you comply with LinkedIn's terms of service and avoid excessive automation that might violate their policies.
This tool is for educational purposes and should be used responsibly.

## Contributors

Sai Teja P
