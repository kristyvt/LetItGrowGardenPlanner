# LetItGrowGardenPlanner

![WelcomeLogo](https://github.com/kristyvt/LetItGrowGardenPlanner/assets/172512085/be1c43b7-4592-409a-a19b-905968c24af5)


The Let it Grow Garden Planner is a digital space where data-driven gardeners can plan what to grow and analyze trends that support their gardening goals.

It is a desktop application that runs on Windows using the Python coding language and a SQL back-end database.

This project was developed as of my Software Develepment degree capstone course at Champlain College Online.

All current Python program files are located in the LetItGrowCodeFiles folder.

Before running the Python program for the first time, please create the database by running the CreateNewGardenDatabase.sql script in SQL Express.

There is a Windows exe file already created. 

To recreate Windows exe:
  Open command prompt and type: cd [installation location]

  Install pip if needed by typing: py -m pip install
  Install pyinstaller: pip install pyinstaller

  Then copy in this command to create the exe:
  pyinstaller --onefile --noconsole --hidden-import babel.numbers --add-data "Images\*.png;.\Images" main.py


Links to Video Walkthroughs
  
Walkthrough of Database: https://1drv.ms/u/s!ApPSXC5kcTPNg6tPYRRvow0BHBOONQ?e=jYbUB0
Walkthrough of Application In Use: https://1drv.ms/u/s!ApPSXC5kcTPNg6tXJlO-MNdUtpgteQ?e=DNjEsv
Walkthrough of Reusable Code: https://1drv.ms/u/s!ApPSXC5kcTPNg6tN-d4dSm_4_mFMfA?e=9Qpp3K
Walkthrough of Data Validation and Verification: https://1drv.ms/u/s!ApPSXC5kcTPNg6tSrJogbA51YIiFTg?e=0mDiGz  
