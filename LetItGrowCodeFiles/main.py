'''
Let it Grow Garden Planner
Garden planning and outcome tracking tool
Kristy Stark
Champlain College SDEV-435-81

Main program launches the interface
and all associated classes.
Last Revised 8/3/24
'''

import sys


class Main:
    def __init__(self):
        import window
        run = window.Window()

        sys.exit(0)


Main()
