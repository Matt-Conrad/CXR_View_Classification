#include "unpackstage.h"

UnpackStage::UnpackStage(ConfigHandler * configHandler) : Stage()
{
    unpacker = new Unpacker(configHandler);
}

void UnpackStage::unpack()
{
    threadpool->start(unpacker);
}
