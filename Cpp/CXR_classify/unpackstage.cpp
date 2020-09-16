#include "unpackstage.h"

UnpackStage::UnpackStage(ConfigHandler * configHandler) : Stage1()
{
    unpacker = new Unpacker(configHandler);
}

void UnpackStage::unpack()
{
    threadpool->start(unpacker);
}
