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
include CMakeFiles/storer.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/storer.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/storer.dir/flags.make

CMakeFiles/storer.dir/storer.cpp.o: CMakeFiles/storer.dir/flags.make
CMakeFiles/storer.dir/storer.cpp.o: /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/storer.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/storer.dir/storer.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/storer.dir/storer.cpp.o -c /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/storer.cpp

CMakeFiles/storer.dir/storer.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/storer.dir/storer.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/storer.cpp > CMakeFiles/storer.dir/storer.cpp.i

CMakeFiles/storer.dir/storer.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/storer.dir/storer.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/storer.cpp -o CMakeFiles/storer.dir/storer.cpp.s

CMakeFiles/storer.dir/storer.cpp.o.requires:

.PHONY : CMakeFiles/storer.dir/storer.cpp.o.requires

CMakeFiles/storer.dir/storer.cpp.o.provides: CMakeFiles/storer.dir/storer.cpp.o.requires
	$(MAKE) -f CMakeFiles/storer.dir/build.make CMakeFiles/storer.dir/storer.cpp.o.provides.build
.PHONY : CMakeFiles/storer.dir/storer.cpp.o.provides

CMakeFiles/storer.dir/storer.cpp.o.provides.build: CMakeFiles/storer.dir/storer.cpp.o


CMakeFiles/storer.dir/confighandler.cpp.o: CMakeFiles/storer.dir/flags.make
CMakeFiles/storer.dir/confighandler.cpp.o: /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/confighandler.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/storer.dir/confighandler.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/storer.dir/confighandler.cpp.o -c /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/confighandler.cpp

CMakeFiles/storer.dir/confighandler.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/storer.dir/confighandler.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/confighandler.cpp > CMakeFiles/storer.dir/confighandler.cpp.i

CMakeFiles/storer.dir/confighandler.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/storer.dir/confighandler.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/confighandler.cpp -o CMakeFiles/storer.dir/confighandler.cpp.s

CMakeFiles/storer.dir/confighandler.cpp.o.requires:

.PHONY : CMakeFiles/storer.dir/confighandler.cpp.o.requires

CMakeFiles/storer.dir/confighandler.cpp.o.provides: CMakeFiles/storer.dir/confighandler.cpp.o.requires
	$(MAKE) -f CMakeFiles/storer.dir/build.make CMakeFiles/storer.dir/confighandler.cpp.o.provides.build
.PHONY : CMakeFiles/storer.dir/confighandler.cpp.o.provides

CMakeFiles/storer.dir/confighandler.cpp.o.provides.build: CMakeFiles/storer.dir/confighandler.cpp.o


CMakeFiles/storer.dir/databasehandler.cpp.o: CMakeFiles/storer.dir/flags.make
CMakeFiles/storer.dir/databasehandler.cpp.o: /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/databasehandler.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/storer.dir/databasehandler.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/storer.dir/databasehandler.cpp.o -c /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/databasehandler.cpp

CMakeFiles/storer.dir/databasehandler.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/storer.dir/databasehandler.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/databasehandler.cpp > CMakeFiles/storer.dir/databasehandler.cpp.i

CMakeFiles/storer.dir/databasehandler.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/storer.dir/databasehandler.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src/databasehandler.cpp -o CMakeFiles/storer.dir/databasehandler.cpp.s

CMakeFiles/storer.dir/databasehandler.cpp.o.requires:

.PHONY : CMakeFiles/storer.dir/databasehandler.cpp.o.requires

CMakeFiles/storer.dir/databasehandler.cpp.o.provides: CMakeFiles/storer.dir/databasehandler.cpp.o.requires
	$(MAKE) -f CMakeFiles/storer.dir/build.make CMakeFiles/storer.dir/databasehandler.cpp.o.provides.build
.PHONY : CMakeFiles/storer.dir/databasehandler.cpp.o.provides

CMakeFiles/storer.dir/databasehandler.cpp.o.provides.build: CMakeFiles/storer.dir/databasehandler.cpp.o


# Object files for target storer
storer_OBJECTS = \
"CMakeFiles/storer.dir/storer.cpp.o" \
"CMakeFiles/storer.dir/confighandler.cpp.o" \
"CMakeFiles/storer.dir/databasehandler.cpp.o"

# External object files for target storer
storer_EXTERNAL_OBJECTS =

libstorer.so: CMakeFiles/storer.dir/storer.cpp.o
libstorer.so: CMakeFiles/storer.dir/confighandler.cpp.o
libstorer.so: CMakeFiles/storer.dir/databasehandler.cpp.o
libstorer.so: CMakeFiles/storer.dir/build.make
libstorer.so: CMakeFiles/storer.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX shared library libstorer.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/storer.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/storer.dir/build: libstorer.so

.PHONY : CMakeFiles/storer.dir/build

CMakeFiles/storer.dir/requires: CMakeFiles/storer.dir/storer.cpp.o.requires
CMakeFiles/storer.dir/requires: CMakeFiles/storer.dir/confighandler.cpp.o.requires
CMakeFiles/storer.dir/requires: CMakeFiles/storer.dir/databasehandler.cpp.o.requires

.PHONY : CMakeFiles/storer.dir/requires

CMakeFiles/storer.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/storer.dir/cmake_clean.cmake
.PHONY : CMakeFiles/storer.dir/clean

CMakeFiles/storer.dir/depend:
	cd /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/src /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build /home/matthew/Documents/CXR_Classification/Combined/DesktopApp/cmake_build/CMakeFiles/storer.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/storer.dir/depend

