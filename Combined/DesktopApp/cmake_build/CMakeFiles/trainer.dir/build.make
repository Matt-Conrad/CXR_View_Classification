# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build

# Include any dependencies generated for this target.
include CMakeFiles/trainer.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/trainer.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/trainer.dir/flags.make

CMakeFiles/trainer.dir/trainer.cpp.o: CMakeFiles/trainer.dir/flags.make
CMakeFiles/trainer.dir/trainer.cpp.o: /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/trainer.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/trainer.dir/trainer.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/trainer.dir/trainer.cpp.o -c /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/trainer.cpp

CMakeFiles/trainer.dir/trainer.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/trainer.dir/trainer.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/trainer.cpp > CMakeFiles/trainer.dir/trainer.cpp.i

CMakeFiles/trainer.dir/trainer.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/trainer.dir/trainer.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/trainer.cpp -o CMakeFiles/trainer.dir/trainer.cpp.s

CMakeFiles/trainer.dir/trainer.cpp.o.requires:

.PHONY : CMakeFiles/trainer.dir/trainer.cpp.o.requires

CMakeFiles/trainer.dir/trainer.cpp.o.provides: CMakeFiles/trainer.dir/trainer.cpp.o.requires
	$(MAKE) -f CMakeFiles/trainer.dir/build.make CMakeFiles/trainer.dir/trainer.cpp.o.provides.build
.PHONY : CMakeFiles/trainer.dir/trainer.cpp.o.provides

CMakeFiles/trainer.dir/trainer.cpp.o.provides.build: CMakeFiles/trainer.dir/trainer.cpp.o


CMakeFiles/trainer.dir/confighandler.cpp.o: CMakeFiles/trainer.dir/flags.make
CMakeFiles/trainer.dir/confighandler.cpp.o: /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/confighandler.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/trainer.dir/confighandler.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/trainer.dir/confighandler.cpp.o -c /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/confighandler.cpp

CMakeFiles/trainer.dir/confighandler.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/trainer.dir/confighandler.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/confighandler.cpp > CMakeFiles/trainer.dir/confighandler.cpp.i

CMakeFiles/trainer.dir/confighandler.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/trainer.dir/confighandler.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/confighandler.cpp -o CMakeFiles/trainer.dir/confighandler.cpp.s

CMakeFiles/trainer.dir/confighandler.cpp.o.requires:

.PHONY : CMakeFiles/trainer.dir/confighandler.cpp.o.requires

CMakeFiles/trainer.dir/confighandler.cpp.o.provides: CMakeFiles/trainer.dir/confighandler.cpp.o.requires
	$(MAKE) -f CMakeFiles/trainer.dir/build.make CMakeFiles/trainer.dir/confighandler.cpp.o.provides.build
.PHONY : CMakeFiles/trainer.dir/confighandler.cpp.o.provides

CMakeFiles/trainer.dir/confighandler.cpp.o.provides.build: CMakeFiles/trainer.dir/confighandler.cpp.o


CMakeFiles/trainer.dir/databasehandler.cpp.o: CMakeFiles/trainer.dir/flags.make
CMakeFiles/trainer.dir/databasehandler.cpp.o: /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/databasehandler.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/trainer.dir/databasehandler.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/trainer.dir/databasehandler.cpp.o -c /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/databasehandler.cpp

CMakeFiles/trainer.dir/databasehandler.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/trainer.dir/databasehandler.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/databasehandler.cpp > CMakeFiles/trainer.dir/databasehandler.cpp.i

CMakeFiles/trainer.dir/databasehandler.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/trainer.dir/databasehandler.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/databasehandler.cpp -o CMakeFiles/trainer.dir/databasehandler.cpp.s

CMakeFiles/trainer.dir/databasehandler.cpp.o.requires:

.PHONY : CMakeFiles/trainer.dir/databasehandler.cpp.o.requires

CMakeFiles/trainer.dir/databasehandler.cpp.o.provides: CMakeFiles/trainer.dir/databasehandler.cpp.o.requires
	$(MAKE) -f CMakeFiles/trainer.dir/build.make CMakeFiles/trainer.dir/databasehandler.cpp.o.provides.build
.PHONY : CMakeFiles/trainer.dir/databasehandler.cpp.o.provides

CMakeFiles/trainer.dir/databasehandler.cpp.o.provides.build: CMakeFiles/trainer.dir/databasehandler.cpp.o


# Object files for target trainer
trainer_OBJECTS = \
"CMakeFiles/trainer.dir/trainer.cpp.o" \
"CMakeFiles/trainer.dir/confighandler.cpp.o" \
"CMakeFiles/trainer.dir/databasehandler.cpp.o"

# External object files for target trainer
trainer_EXTERNAL_OBJECTS =

libtrainer.so: CMakeFiles/trainer.dir/trainer.cpp.o
libtrainer.so: CMakeFiles/trainer.dir/confighandler.cpp.o
libtrainer.so: CMakeFiles/trainer.dir/databasehandler.cpp.o
libtrainer.so: CMakeFiles/trainer.dir/build.make
libtrainer.so: CMakeFiles/trainer.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX shared library libtrainer.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/trainer.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/trainer.dir/build: libtrainer.so

.PHONY : CMakeFiles/trainer.dir/build

CMakeFiles/trainer.dir/requires: CMakeFiles/trainer.dir/trainer.cpp.o.requires
CMakeFiles/trainer.dir/requires: CMakeFiles/trainer.dir/confighandler.cpp.o.requires
CMakeFiles/trainer.dir/requires: CMakeFiles/trainer.dir/databasehandler.cpp.o.requires

.PHONY : CMakeFiles/trainer.dir/requires

CMakeFiles/trainer.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/trainer.dir/cmake_clean.cmake
.PHONY : CMakeFiles/trainer.dir/clean

CMakeFiles/trainer.dir/depend:
	cd /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build/CMakeFiles/trainer.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/trainer.dir/depend
