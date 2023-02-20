import dicom2nifti
import streamlit as st
import subprocess
# import pydicom
import nibabel as nib
import torch
import time
import sys
import os


dicom_folder = './dicom'
nifti_folder = './nifti'


IN_VOLUME="dest/in_volume.nii.gz"
BET_INPUT_VOLUME="./T1w_norm.nii.gz"
MASK_VOLUME="./T1w_norm_noskull_mask.nii.gz"

IN_VOLUME_CROP="dest/T1w_norm_noskull_cropped.nii.gz"
MASK_VOLUME ="dest/in_volume_mask.nii.gz"

LOW_MEM_ARG = "--lowmem True" 
SUBJECT_ID = st.text_input('Subject ID', 'sub-001')

THICK_VOLUME= "dest/T1w_thickmap.nii.gz"


# Create destination folder if it doesn't exist
if not os.path.exists(dicom_folder):
    os.makedirs(dicom_folder)

if not os.path.exists(nifti_folder):
    os.makedirs(nifti_folder)

if not os.path.exists("dest"):
    os.makedirs('dest')

uploaded_files = st.file_uploader('Choose files', accept_multiple_files=True)

# Save uploaded files to destination folder
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(dicom_folder, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.read())
       
# making sure the dicom folder isnt emptpy       
if not os.listdir(dicom_folder):
    st.write(f'{dicom_folder} is empty')
else:
    st.write(f'{dicom_folder} is not empty')


st.write("="*50)

st.title('DICOM to NIfTI Converter')

if st.button("Convert"):
    st.write(f'Converting DICOM files in {dicom_folder}...')

    # Convert to NIfTI
    dicom2nifti.convert_directory(dicom_folder, nifti_folder, compression=True, reorient=True)
    
    # Save NIfTI file
    # nifti_filename = f'{output_file}.nii.gz'
    st.write(os.listdir(nifti_folder))
    st.success(f'Conversion complete!')

st.write("="*50)


gpu_available = torch.cuda.is_available()

st.write("# Cortex Measuring App")

st.write(f"is GPU available: {gpu_available}")
if gpu_available == False:
  st.write("The App will take take longer time than with GPU")

st.write("="*50)


if st.button('do all'):
    uploaded_file = os.listdir(nifti_folder)[0]
    st.write(f"file is {uploaded_file}")
    st.write(subprocess.run([f"{sys.executable}", "src/conform.py", uploaded_file, "./T1w_norm.nii.gz" ],
                          stdout = sys.stdout, stderr= subprocess.PIPE) )
    st.write("Done conforming")
    st.write(subprocess.run([f"{sys.executable} src/bet.py {BET_INPUT_VOLUME} {IN_VOLUME} "],
                          stdout = sys.stdout, stderr= subprocess.PIPE, shell = True) )
    st.write("Done Skull stripping")
    st.write(subprocess.run([f"{sys.executable} src/crop.py {MASK_VOLUME} {IN_VOLUME} {IN_VOLUME_CROP}"],
                        stdout= sys.stdout, stderr = subprocess.PIPE, shell = True) ) 
    st.write(subprocess.run([f"{sys.executable} src/DeepSCAN_Anatomy_Newnet_apply.py {LOW_MEM_ARG} {IN_VOLUME_CROP} dest/ {SUBJECT_ID}"] ,
            stdout= sys.stdout, stderr = subprocess.PIPE, shell = True) ) 
    st.write(subprocess.run([f"{sys.executable} src/DiReCT.py dest/ dest/ "], 
          stdout= sys.stdout, stderr = subprocess.PIPE, shell = True) ) 
    st.write("Done DiReCT")

    # st.write(subprocess.run([f"{sys.executable} src/extract_stats.py {THICK_VOLUME} dest/seg.nii.gz dest/softmax_seg.nii.gz {SUBJECT_ID}"],
    #           stdout= sys.stdout, stderr = subprocess.PIPE, shell = True) ) 

    st.write(os.listdir())
    st.write(os.listdir("dest"))

    
st.write("="*50)


uploaded_file = st.file_uploader("Upload a Nifti file")
if uploaded_file != None:

  file_name = uploaded_file.name
  path = os.path.join(os.getcwd(), file_name)
  st.write(path)
  if st.button('Print file name'):
    st.write(file_name)


  with open(path,"wb") as f:
          f.write(uploaded_file.getbuffer())
   #===================

  if st.button("Conform Nifti"):
    st.write(subprocess.run([f"{sys.executable}", "src/conform.py", uploaded_file.name, "./T1w_norm.nii.gz" ],
                            stdout = sys.stdout, stderr= subprocess.PIPE) )
    st.write("Done conforming")

  
  if st.button("Skull Strip", key = 'abc'):
    st.write(subprocess.run([f"{sys.executable} src/bet.py {BET_INPUT_VOLUME} {IN_VOLUME} "],
                            stdout = sys.stdout, stderr= subprocess.PIPE, shell = True) )
    st.write("Done Skull stripping")
  # # st.write(subprocess.run(["python src/conform.py 80100000_t1w_3d_tfe_nyul.nii.gz T1w_norm.nii.gz "],  stdout = subprocess.PIPE, stderr= subprocess.PIPE, shell=False) )
  # # st.write(subprocess.run(["dl+direct", "--subject", "001", "--lowmem", "--bet", "/content/drive/MyDrive/Hipposeg/patient_data/80100000_t1w_3d_tfe_nyul.nii.gz"], stdout = subprocess.PIPE, stderr= subprocess.PIPE, shell=True))

  IN_VOLUME_CROP="dest/T1w_norm_noskull_cropped.nii.gz"
  MASK_VOLUME ="dest/in_volume_mask.nii.gz"
  
  if st.button("Skull Strip", key = 'cab'):
    st.write(subprocess.run([f"{sys.executable} src/crop.py {MASK_VOLUME} {IN_VOLUME} {IN_VOLUME_CROP}"],
                          stdout= sys.stdout, stderr = subprocess.PIPE, shell = True) ) 

  if st.button("DeepScan segmentation", key = 'bca'):
    LOW_MEM_ARG = "--lowmem True" 
    SUBJECT_ID = st.text_input('Subject ID', 'sub-001')
    st.write(subprocess.run([f"{sys.executable} src/DeepSCAN_Anatomy_Newnet_apply.py {LOW_MEM_ARG} {IN_VOLUME_CROP} dest/ {SUBJECT_ID}"] ,
             stdout= sys.stdout, stderr = subprocess.PIPE, shell = True) ) 

  if st.button("DiReCT", key = 'cba'):
    st.write(subprocess.run([f"{sys.executable} src/DiReCT.py dest/ dest/ "], 
            stdout= sys.stdout, stderr = subprocess.PIPE, shell = True) ) 
    st.write("Done DiReCT")

    THICK_VOLUME= "dest/T1w_thickmap.nii.gz"
    if st.button("Extract Stats", key = 'acb'):
      st.write(subprocess.run([f"{sys.executable} src/extract_stats.py {THICK_VOLUME} dest/seg.nii.gz dest/softmax_seg.nii.gz {SUBJECT_ID}"],
                stdout= sys.stdout, stderr = subprocess.PIPE, shell = True) ) 

  
  # st.markdown("# maybe it worked")
  st.write(os.listdir())
  st.write(os.listdir("dest"))

  # st.write(subprocess.run(["dl_direct"], stdout = subprocess.PIPE, stderr= subprocess.PIPE, shell=True))
