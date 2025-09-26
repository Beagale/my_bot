## From Abby

(As of September 22nd, check commit history for newest changes)

Skipped over the following 3 tutorials, so code written from these tutorials might be missing atm:

(Using ros2_control to drive robot (off the edge of the table)): https://www.youtube.com/watch?v=4VVrTCnxvSw&list=PLunhqkrRNRhYAffV8JDiFOatQXuU-NnxT&index=14

(Easy wireless control for your homemade robot): https://www.youtube.com/watch?v=F5XlNiCKbrY&list=PLunhqkrRNRhYAffV8JDiFOatQXuU-NnxT&index=15

(Control your ROS robot from your phone): https://www.youtube.com/watch?v=F5XlNiCKbrY&list=PLunhqkrRNRhYAffV8JDiFOatQXuU-NnxT&index=15

In addition, code written for the physical robot may also be missing in this repo (ex. launch file for camera), as I could only follow the parts of the tutorials that featured simulation at the time (late August).

## Robot Package Template

This is a GitHub template. You can make your own copy by clicking the green "Use this template" button.

It is recommended that you keep the repo/package name the same, but if you do change it, ensure you do a "Find all" using your IDE (or the built-in GitHub IDE by hitting the `.` key) and rename all instances of `my_bot` to whatever your project's name is.

Note that each directory currently has at least one file in it to ensure that git tracks the files (and, consequently, that a fresh clone has direcctories present for CMake to find). These example files can be removed if required (and the directories can be removed if `CMakeLists.txt` is adjusted accordingly).
