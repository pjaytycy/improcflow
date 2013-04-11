import numpy
import cv2
from cv2 import cv

# convert FROM / TO
#   (nested) python list
#   IplImage
#   CvMat
#   NumPy array

def get_source_data_type(value):
  if isinstance(value, list):
    return list
  if isinstance(value, numpy.ndarray):
    return numpy.ndarray
  if isinstance(value, cv.cvmat):
    return cv.cvmat
  if isinstance(value, cv.iplimage):
    return cv.iplimage
  return None

# LIS => NPA  numpy.array(value)
# NPA => LIS  value.tolist()

# NPA => CVM  cv.fromarray(value)
# CVM => NPA  numpy.asarray(value)

# CVM => IPL  cv.GetImage(value)
# IPL => CVM  cv.GetMat(value)

# LIS => CVM    LIS->NPA->CVM
# CVM => LIS    CVM->NPA->LIS
# NPA => IPL    NPA->CVM->IPL
# IPL => NPA    IPL->CVM->NPA
# LIS => IPL    LIS->NPA->CVM->IPL
# IPL => LIS    IPL->CVM->NPA->LIS


def convert_data(value, dst_data_types):
  if dst_data_types is None:
    return value
  
  src_data_type = get_source_data_type(value)
  if src_data_type in dst_data_types:
    return value
  
  if src_data_type == list:
    return convert_data_from_list(value, dst_data_types)
  if src_data_type == numpy.ndarray:
    return convert_data_from_array(value, dst_data_types)
  if src_data_type == cv.cvmat:
    return convert_data_from_cvmat(value, dst_data_types)
  if src_data_type == cv.iplimage:
    return convert_data_from_iplimage(value, dst_data_types)

def convert_data_from_list(value, dst_data_types):
  npa_value = numpy.array(value)
  if numpy.ndarray in dst_data_types:
    return npa_value
    
  return convert_data_from_array(npa_value, dst_data_types)

def convert_data_from_array(value, dst_data_types):
  if list in dst_data_types:
    return value.tolist()
  
  cvm_value = cv.fromarray(value)
  if cv.cvmat in dst_data_types:
    return cvm_value
  
  return convert_data_from_cvmat(cvm_value, dst_data_types)

def convert_data_from_cvmat(value, dst_data_types):
  if cv.iplimage in dst_data_types:
    return cv.GetImage(value)
  
  npa_value = numpy.asarray(value)
  if numpy.ndarray in dst_data_types:
    return npa_value
  
  return convert_data_from_array(npa_value, dst_data_types)

def convert_data_from_iplimage(value, dst_data_types):
  cvm_value = cv.GetMat(value)
  if cv.cvmat in dst_data_types:
    return cvm_value
  
  return convert_data_from_cvmat(cvm_value, dst_data_types)
  