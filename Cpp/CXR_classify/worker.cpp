#include "worker.h"
#include "iostream"
#include "appcontroller.h"

//Worker::Worker(void (*fun_ptr) ()) : QRunnable()
//{
//    Worker::fun_ptr = fun_ptr;
//}

//void Worker::run()
//{
//    (*Worker::fun_ptr)();
//}



Worker::Worker(AppController * controller) { // Constructor
    Worker::controller = controller;
}

Worker::~Worker() { // Destructor
    // free resources
}

void Worker::process() { // Process. Start processing data.
    // allocate resources using new here
    controller->downloader->getDataset();
    emit finished();
}
