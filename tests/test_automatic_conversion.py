from django.test import TestCase

from improcflow.logic import convert_data

import numpy
from cv2 import cv


class AutomaticConversionTests(TestCase):
  src_list  = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
  src_array = numpy.array(src_list)
  src_mat   = cv.fromarray(src_array)
  src_ipl   = cv.GetImage(src_mat)
  
  def test_list_to_None(self):
    dst = convert_data(self.src_list, None)
    self.assertEqual(type(dst), list)
    
  def test_list_to_list(self):
    dst = convert_data(self.src_list, [list])
    self.assertEqual(type(dst), list)
    
  def test_list_to_array(self):
    dst = convert_data(self.src_list, [numpy.ndarray])
    self.assertEqual(type(dst), numpy.ndarray)
  
  def test_list_to_cvmat(self):
    dst = convert_data(self.src_list, [cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_list_to_iplimage(self):
    dst = convert_data(self.src_list, [cv.iplimage])
    self.assertEqual(type(dst), cv.iplimage)
  
  def test_list_to_cvmat_or_iplimage(self):
    dst = convert_data(self.src_list, [cv.cvmat, cv.iplimage])
    self.assertEqual(type(dst), cv.cvmat)
    
  def test_list_to_iplimage_or_cvmat(self):
    dst = convert_data(self.src_list, [cv.iplimage, cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_array_to_None(self):
    dst = convert_data(self.src_array, None)
    self.assertEqual(type(dst), numpy.ndarray)
    
  def test_array_to_list(self):
    dst = convert_data(self.src_array, [list])
    self.assertEqual(type(dst), list)
    
  def test_array_to_array(self):
    dst = convert_data(self.src_array, [numpy.ndarray])
    self.assertEqual(type(dst), numpy.ndarray)
  
  def test_array_to_cvmat(self):
    dst = convert_data(self.src_array, [cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_array_to_iplimage(self):
    dst = convert_data(self.src_array, [cv.iplimage])
    self.assertEqual(type(dst), cv.iplimage)
  
  def test_array_to_cvmat_or_iplimage(self):
    dst = convert_data(self.src_array, [cv.cvmat, cv.iplimage])
    self.assertEqual(type(dst), cv.cvmat)
    
  def test_array_to_iplimage_or_cvmat(self):
    dst = convert_data(self.src_array, [cv.iplimage, cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_cvmat_to_None(self):
    dst = convert_data(self.src_mat, None)
    self.assertEqual(type(dst), cv.cvmat)
    
  def test_cvmat_to_list(self):
    dst = convert_data(self.src_mat, [list])
    self.assertEqual(type(dst), list)
    
  def test_cvmat_to_array(self):
    dst = convert_data(self.src_mat, [numpy.ndarray])
    self.assertEqual(type(dst), numpy.ndarray)
  
  def test_cvmat_to_cvmat(self):
    dst = convert_data(self.src_mat, [cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_cvmat_to_iplimage(self):
    dst = convert_data(self.src_mat, [cv.iplimage])
    self.assertEqual(type(dst), cv.iplimage)
  
  def test_cvmat_to_cvmat_or_iplimage(self):
    dst = convert_data(self.src_mat, [cv.cvmat, cv.iplimage])
    self.assertEqual(type(dst), cv.cvmat)
    
  def test_cvmat_to_iplimage_or_cvmat(self):
    dst = convert_data(self.src_mat, [cv.iplimage, cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_iplimage_to_None(self):
    dst = convert_data(self.src_ipl, None)
    self.assertEqual(type(dst), cv.iplimage)
    
  def test_iplimage_to_list(self):
    dst = convert_data(self.src_ipl, [list])
    self.assertEqual(type(dst), list)
    
  def test_iplimage_to_array(self):
    dst = convert_data(self.src_ipl, [numpy.ndarray])
    self.assertEqual(type(dst), numpy.ndarray)
  
  def test_iplimage_to_cvmat(self):
    dst = convert_data(self.src_ipl, [cv.cvmat])
    self.assertEqual(type(dst), cv.cvmat)
  
  def test_iplimage_to_iplimage(self):
    dst = convert_data(self.src_ipl, [cv.iplimage])
    self.assertEqual(type(dst), cv.iplimage)
  
  def test_iplimage_to_cvmat_or_iplimage(self):
    dst = convert_data(self.src_ipl, [cv.cvmat, cv.iplimage])
    self.assertEqual(type(dst), cv.iplimage)
    
  def test_iplimage_to_iplimage_or_cvmat(self):
    dst = convert_data(self.src_ipl, [cv.iplimage, cv.cvmat])
    self.assertEqual(type(dst), cv.iplimage)
