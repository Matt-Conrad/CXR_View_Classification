import logging
import os
import json
from PyQt5.QtCore import pyqtSlot
from stage import Stage, Runnable
from ctypes import cdll
import time

class LabelStage(Stage):
    """Downloads datasets from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self)
        if configHandler.getDatasetType() == "subset":
            self.labeler = self.ManualLabeler(configHandler, dbHandler)
        elif configHandler.getDatasetType() == "full_set":
            self.labeler = self.LabelImporter(configHandler, dbHandler)
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')

    @pyqtSlot()
    def label(self):
        self.threadpool.start(self.labeler)

    class LabelImporter(Runnable):
        """Class for importing image labels from CSV."""
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)

            self.lib = cdll.LoadLibrary(os.path.join(configHandler.getParentFolder(), "cmake_build", "liblabelimporter.so"))
            
            self.obj = self.lib.LabelImporter_new()
        
        @pyqtSlot()
        def run(self):
            logging.info("Importing label data from CSV")
            self.signals.attemptUpdateProBarBounds.emit(0,1)
            self.signals.attemptUpdateProBarValue.emit(0)
            self.signals.attemptUpdateText.emit("Importing label data")

            start = time.time()
            self.lib.LabelImporter_run(self.obj)
            end = time.time()
            print(end - start)
            
            self.signals.attemptUpdateProBarValue.emit(1)
            self.signals.attemptUpdateText.emit("Done importing")
            self.signals.finished.emit()
            logging.info("Done importing label data")

    class ManualLabeler(Runnable):
        """Class used to assist in labeling the data."""
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)

            self.count = 0
            self.records = None
            self.record = None

        @pyqtSlot()
        def run(self):
            """Displays the content into the window."""
            logging.info('Filling window')
            self.queryImageList()
            
            self.signals.attemptUpdateText.emit("Please manually label images")
            self.signals.attemptUpdateProBarBounds.emit(0, self.expectedNumFiles)

            self.dbHandler.addTableToDb(self.configHandler.getTableName('label'), self.configHandler.getColumnsInfoFullPath(), "nonElementColumns", 'labels')
            
            self.displayNextImage()

            while self.count < self.expectedNumFiles:
                pass

            logging.info('End of query')
            self.signals.attemptUpdateText.emit("Image labeling complete")
            self.signals.finished.emit()

        def frontal(self):
            logging.debug('Front')
            self.storeLabel('F')
            self.count += 1
            self.displayNextImage()
            
        def lateral(self):
            logging.debug('Lateral')
            self.storeLabel('L')
            self.count += 1
            self.displayNextImage()

        def displayNextImage(self):
            logging.debug('Image count: ' + str(self.count))
            self.signals.attemptUpdateText.emit('Image Count: ' + str(self.count))
            self.signals.attemptUpdateProBarValue.emit(self.dbHandler.countRecords(self.configHandler.getTableName('label')))

            if self.count < self.expectedNumFiles:
                self.record = self.records[self.count]
                self.signals.attemptUpdateImage.emit(self.record)
        
        def queryImageList(self):
            logging.debug('Getting the image list')
            sqlQuery = 'SELECT file_path, bits_stored FROM ' + self.configHandler.getTableName("metadata") + ' ORDER BY file_path;'
            self.records = self.dbHandler.executeQuery(self.dbHandler.connection, sqlQuery).fetchall()

        def storeLabel(self, decision):
            logging.debug('Storing label')
            sqlQuery = 'INSERT INTO ' + self.configHandler.getTableName("label") + ' (file_name, file_path, image_view) VALUES (\'' + self.record['file_path'].split(os.sep)[-1] + '\', \'' + self.record['file_path'] + '\', \'' + decision + '\');'
            self.dbHandler.executeQuery(self.dbHandler.connection, sqlQuery)
