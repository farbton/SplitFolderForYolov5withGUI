# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 12:36:26 2024

@author: Admin
"""

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog,\
    QGraphicsPixmapItem, QGridLayout, QLabel, QGraphicsItem, QGraphicsTextItem
from PyQt5.QtGui import QPixmap, QPen, QFont, QImage, QColor
from PIL import Image, ImageEnhance , ImageQt, ImageShow
import os, numpy as np
import time
import io
import splitfolder
import fnmatch

class Window(QMainWindow):
    
    def __init__(self, app):       
        super(Window, self).__init__()       
        uic.loadUi("splitFolderGui.ui", self)
        self.source_folder_path = "source/"
        self.destination_folder_images_path = "destination/images/"
        self.destination_folder_labels_path = "destination/labels/"
        self.setWindowTitle("Split Folder Tool for YOLOv5")
        self.screen = app.primaryScreen()
        self.init_paths()
        
    def init_paths(self):
        self.source_folder_path = os.getcwd() + "/" + self.source_folder_path
        self.lb_source_folder_path.setText(self.source_folder_path)
        
        self.destination_folder_images_path = os.getcwd() + "/" + self.destination_folder_images_path
        self.lb_destination_folder_images_path.setText(self.destination_folder_images_path)
        
        
        self.destination_folder_labels_path = os.getcwd() + "/" + self.destination_folder_labels_path
        self.lb_destination_folder_labels_path.setText(self.destination_folder_labels_path)
                    
    def start(self):
        self.pb_select_source_folder.clicked.connect(self.open_sourcefolder)
        self.pb_select_destination_folder_images.clicked.connect(self.open_destinationfolder_images)
        self.pb_select_destination_folder_labels.clicked.connect(self.open_destinationfolder_labels)
        self.pb_split.clicked.connect(self.split)
        
    def open_sourcefolder(self):
        dir = QFileDialog.getExistingDirectory()
        
        if dir:
            self.source_folder_path = dir+"/"
            
        if self.source_folder_path:
            self.print_text_in_console("source folder path: " + self.source_folder_path)
            self.lb_source_folder_path.setText(self.source_folder_path)
            numbers = len(fnmatch.filter(os.listdir(self.source_folder_path), "*.txt"))
            self.lb_console.setText(self.lb_console.text() + "\n" + "files in source folder: " + str(numbers))
    
    def open_destinationfolder_images(self):
        dir = QFileDialog.getExistingDirectory()
        
        if dir:
            self.destination_folder_images_path = dir+"/"
            
        if self.destination_folder_images_path:
            self.print_text_in_console("destination folder path: " + self.destination_folder_images_path)
            self.lb_destination_folder_images_path.setText(self.destination_folder_images_path)
       
            
    
    def open_destinationfolder_labels(self):
        dir = QFileDialog.getExistingDirectory()
        
        if dir:
            self.destination_folder_labels_path = dir+"/"
            
        if self.destination_folder_labels_path:
            self.print_text_in_console("destination folder path: " + self.destination_folder_labels_path)
            self.lb_destination_folder_labels_path.setText(self.destination_folder_labels_path)
    
    def print_text_in_console(self, text):
        self.lb_console.setText(self.lb_console.text() + "\n" + text)
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
        
    def split(self):
        self.splitfolder = splitfolder.Splitfolder(self, 
                                                   self.source_folder_path, 
                                                   self.destination_folder_images_path, 
                                                   self.destination_folder_labels_path)
        
