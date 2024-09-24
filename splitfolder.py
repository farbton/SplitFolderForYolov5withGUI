# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 11:09:02 2023

@author: Kirko
"""

import os
import random
import shutil
from PyQt5 import QtCore

# source_dir = "C:/Users/Admin/Nextcloud/Gemeinsame Dateien/Fg-Medientechnik_Lehrstuhl/3_Projekte/KI@MINT/Praktikum/Haribo_Orginalaufnahmen/allInOne/"
# output_dir = "C:/KI_MINT/Git/split_test"



   
class Splitfolder(QtCore.QObject):
    def __init__(self, main_window, app, source_folder_path, destination_folder_images_path, destination_folder_labels_path):       
        QtCore.QObject.__init__(self)
        self.main_window = main_window
        self.app = app
        self.source_folder_path = source_folder_path
        self.destination_folder_images_path = destination_folder_images_path
        self.destination_folder_labels_path = destination_folder_labels_path
        self.create_train_test_val_folder()
        self.list_filenames = []
        self.list_train      = None
        self.list_test       = None
        self.list_val        = None
        self.number_of_train = None
        self.number_of_test  = None
        self.number_of_val   = None
        self.get_list_of_filenames()
        self.shuffle_files()
        self.split_list_filenames()
        self.copy_files()
        
    def create_train_test_val_folder(self):
        """
        Check if exist the train, test and val folder
        if not, create it
    
        """
        path_train_images = os.path.join(self.destination_folder_images_path, "train")
        path_test_images  = os.path.join(self.destination_folder_images_path, "test")
        path_val_images   = os.path.join(self.destination_folder_images_path, "val")
        
        path_train_labels = os.path.join(self.destination_folder_labels_path, "train")
        path_test_labels  = os.path.join(self.destination_folder_labels_path, "test")
        path_val_labels   = os.path.join(self.destination_folder_labels_path, "val")
        
        
        if not os.path.exists(path_train_images):
            os.mkdir(path_train_images)
            self.main_window.lb_console.setText(
                self.main_window.lb_console.text() + "\n"\
                    + "create: images/train")
        if not os.path.exists(path_test_images):
            os.mkdir(path_test_images)
            self.main_window.lb_console.setText(
                self.main_window.lb_console.text() + "\n"\
                    + "create: images/test")
        if not os.path.exists(path_val_images):
            os.mkdir(path_val_images)
            self.main_window.lb_console.setText(
                self.main_window.lb_console.text() + "\n"\
                    + "create: images/val")
            
        if not os.path.exists(path_train_labels):
            os.mkdir(path_train_labels)
            self.main_window.lb_console.setText(
                self.main_window.lb_console.text() + "\n"\
                    + "create: labels/train")
        if not os.path.exists(path_test_labels):
            os.mkdir(path_test_labels)
            self.main_window.lb_console.setText(
                self.main_window.lb_console.text() + "\n"\
                    + "create: labels/test")
        if not os.path.exists(path_val_labels):
            os.mkdir(path_val_labels)
            self.main_window.lb_console.setText(
                self.main_window.lb_console.text() + "\n"\
                    + "create: labels/val")
    
    def get_list_of_filenames(self):
        """
        read all image filename in one list
    
        """
        for filename in os.listdir(self.source_folder_path):
            if filename.endswith(".jpg"):
                self.list_filenames.append(filename)
        self.main_window.lb_console.setText(
            self.main_window.lb_console.text() + "\n" + "numbers of files: " + str(len(self.list_filenames)))
                
    def shuffle_files(self):
        """
        shuffle the list_filenames for random distribution
    
        """
        random.seed(4)
        random.shuffle(self.list_filenames)
        # print(self.list_filenames)
                
    
    def split_list_filenames(self):
        """
        split the list_filenames for train, test and val set
        and create new lists for train, test and val
    
        """
        # global number_of_train, number_of_test, number_of_val, \
        #     list_train, list_test, list_val
            
        self.number_of_train = int(0.8 * len(self.list_filenames))
        self.number_of_test  = int(0.1 * len(self.list_filenames))
        self.number_of_val   = int(0.1 * len(self.list_filenames))
        
        self.list_train = self.list_filenames[0:self.number_of_train]
        self.list_test  = self.list_filenames[self.number_of_train:(self.number_of_train + self.number_of_test)]
        self.list_val   = self.list_filenames[-self.number_of_val:]
        
    def copy_files(self):
        """
        copy the .jpg + .txt in seperated folder for train, test and val
    
        """
        n_train = len(self.list_train)
        n_test = len(self.list_test)
        n_val = len(self.list_val)
        self.main_window.progressBar.reset()
        self.main_window.progressBar.setRange(0, (n_train + n_test + n_val))

        
        for count, file in enumerate(self.list_train):
            name, ext = os.path.splitext(file)
            txt_file  = name + ".txt"
            shutil.copy(self.source_folder_path + file, self.destination_folder_images_path + "/train")
            shutil.copy(self.source_folder_path + txt_file, self.destination_folder_labels_path + "/train")
            self.main_window.progressBar.setValue(count+1)
            self.app.processEvents()
            # print(count)
            # print(len(self.list_train))
            
        self.print_text_in_console("number of train images: " + str(self.number_of_train))
            
        for count, file in enumerate(self.list_test):
            name, ext = os.path.splitext(file)
            txt_file  = name + ".txt"
            shutil.copy(self.source_folder_path + file, self.destination_folder_images_path + "/test")
            shutil.copy(self.source_folder_path + txt_file, self.destination_folder_labels_path + "/test")
            self.main_window.progressBar.setValue(n_train + count+1)
            self.app.processEvents()
            
        self.print_text_in_console("number of test images: " + str(self.number_of_test))
            
        for count, file in enumerate(self.list_val):
            name, ext = os.path.splitext(file)
            txt_file  = name + ".txt"
            shutil.copy(self.source_folder_path + file, self.destination_folder_images_path + "/val")
            shutil.copy(self.source_folder_path + txt_file, self.destination_folder_labels_path + "/val")
            self.main_window.progressBar.setValue(n_train + n_test + count+1)
            self.app.processEvents()
            
        self.print_text_in_console("number of val images: " + str(self.number_of_val))    
    
    def print_text_in_console(self, text):
        self.main_window.lb_console.setText(self.main_window.lb_console.text() + "\n" + text)
        self.main_window.scrollArea.verticalScrollBar().setValue(self.main_window.scrollArea.verticalScrollBar().maximum())
        
    # if __name__ == "__main__":
    #     create_train_test_val_folder()
    #     get_list_of_filenames()
    #     shuffle_files()
    #     split_list_filenames()
    #     copy_files()
    #     print("all images: " , len(list_filenames))
    #     print("images for train: " , number_of_train)
    #     print("images for test:  "  , number_of_test)
    #     print("images for val:   "   , number_of_val)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    