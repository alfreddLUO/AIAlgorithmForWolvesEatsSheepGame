


####  PYTHON   #### 
# how to run this game? In any python>=3.6 environment
1. pip install pygame
2. python WES_Main.py

--------------------------------------------------------------------------
We highly recommend building the AI algorithm using Python. 
Here are one strategy on how to call AI algorithms with C++ or Java in Python. Note that there are other solutions available to call C++ or Java in Python.
--------------------------------------------------------------------------

####  C++   #### 
If you don't have a g++ environment on Windows, you can use a cross-compiler like MinGW-w64 to compile your code and create the shared library. Here are the steps to do this:

1. Download and install MinGW-w64: You can download it from the official website https://sourceforge.net/projects/mingw-w64/. Choose the appropriate version (32-bit or 64-bit) based on your system architecture and install it.

2. Set the PATH environment variable: After installing MinGW-w64, you need  a) Open the Start menu and search for "Environment Variables".
to set the PATH environment variable to include the bin directory of the MinGW-w64 installation. To do this, follow these steps:
 b) Click on "Edit the system environment variables".
 c) Click on the "Environment Variables" button.
 d) Under "System variables", scroll down to find the "Path" variable and click on "Edit".
 e) Click on "New" and add the path to the bin directory of the MinGW-w64 installation (e.g., C:\mingw-w64\x86_64-8.1.0-win32-seh-rt_v6-rev0\mingw64\bin).
 f) Click on "OK" to close all windows.

3. Compile the code: Open a command prompt and navigate to the directory containing your aiAlgorithm.cpp file. Then, use the following command to compile the code and create the shared library:
g++ --shared -o aiAlgorithm.so aiAlgorithm.cpp

####  JAVA   ####

Note that you need to have the 'AIAlgorithm' class defined in a Java file and compiled into a '.class' file before you can use it in Python with JPype. Also, you need to make sure that the class and method names are spelled correctly.

To compile a Java file containing the 'AIAlgorithm' class to a '.class' file, you can use the Java compiler javac that comes with the Java Development Kit (JDK). Here are the steps:

1. Install the JDK on your computer if you haven't already. You can download it from the Oracle website or your operating system's package manager.

2. Open a command prompt or terminal window.

3. Navigate to the directory that contains the Java file you want to compile. For example, if the file is located in 'C:\myproject', you can navigate to that directory by running 'cd C:\myproject on Windows' or 'cd /path/to/myproject' on Unix-based systems.

4. Run the 'javac' command followed by the name of the Java file you want to compile. For example, if the file is named 'AIAlgorithm.java', you can run 'javac AIAlgorithm.java'. This will compile the Java file and generate a corresponding '.class' file in the same directory.

5. If the compilation succeeds without errors, you should see a new file named 'AIAlgorithm.class' in the same directory as the Java file. You can now use this file as needed, for example by running it with the 'java' command: 'java AIAlgorithm'.

6. Use the following command to compile the '.class' to '.jar' file: "jar cf AIAlgorithm.jar AIAlgorithm.class"