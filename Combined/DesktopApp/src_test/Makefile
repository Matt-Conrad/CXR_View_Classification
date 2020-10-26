CXX = g++
CXXFLAGS = -std=c++17 -fPIC

TARGET = unpacker

# libdownloader.so: downloader.o confighandler.o
# 	$(CXX) $(CXXFLAGS) -o libdownloader.so downloader.o confighandler.o

$(TARGET).o: $(TARGET).h 
	$(CXX) $(CXXFLAGS) -c $(TARGET).cpp -o $(TARGET).o