# LetItGrowGardenPlanner

![WelcomeLogo](https://github.com/kristyvt/LetItGrowGardenPlanner/assets/172512085/be1c43b7-4592-409a-a19b-905968c24af5)


The Let it Grow Garden Planner is a digital space where data-driven gardeners can plan what to grow and analyze trends that support their gardening goals.

It is a desktop application that runs on Windows using the Python coding language and a SQL back-end database.

This project was developed as of my Software Develepment degree capstone course at Champlain College Online.

All current Python program files are located in the LetItGrowCodeFiles folder.

Before running the Python program for the first time, please create the database by running the CreateNewGardenDatabase.sql script in SQL Express.

To Create Windows exe:
  Open command prompt and type: cd [installation location]

  Install pip if needed by typing: py -m pip install
  Install pyinstaller: pip install pyinstaller

  Then copy in this command to create the exe:
  pyinstaller --onefile --noconsole --hidden-import babel.numbers --add-data "Images\*.png;.\Images" main.py



Links to Video Walkthroughs
  
Walkthrough of Database: https://1drv.ms/v/s!ApPSXC5kcTPNg6pL-vlho_QvyvVqOA?e=RWBgTT

Walkthrough of Application In Use: https://1drv.ms/v/s!ApPSXC5kcTPNg6s7kEg0qlN17g7AAA?e=463dtN

Walkthrough of Reusable Code: https://1drv.ms/v/s!ApPSXC5kcTPNg6s8Rm_fRWVUAzdPpw?e=xX2nCj

Walkthrough of Data Validation and Verification: https://1drv.ms/v/s!ApPSXC5kcTPNg6s-rbXuJZexiEje4w?e=1M0ISd


Project Documentation File

[ProjectDocumentation_KStark.pdf](https://github.com/user-attachments/files/16573531/ProjectDocumentation_KStark.pdf)

