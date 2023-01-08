import streamlit as st
import subprocess
import torch
import time
import sys
import os

gpu_available = torch.cuda.is_available()


st.write("# Cortex Measuring App")

st.write(f"is GPU available: {gpu_available}")
if gpu_available == False:
  st.write("The App will take take longer time than with GPU")

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

  # st.write('## Run Streamlit on Colab with `pyngrok` ')
  # st.write("This is an amazing tutorial, I love this channel!!!")
  # st.write(subprocess.run(["dl+direct"] ))
  if st.button('use bash'):
    st.write(subprocess.run([f"bash dl+direct.sh --subject 001 --lowmem --bet ./{uploaded_file.name} dest"],
         stdout= sys.stdout, stderr = sys.stderr, shell = True) ) 
         
  if st.button("Conform Nifti"):
    st.write(subprocess.run([f"{sys.executable}", "src/conform.py", uploaded_file.name, "./T1w_norm.nii.gz" ],
                            stdout = sys.stdout, stderr= subprocess.PIPE) )
    st.write("Done conforming")

  
  IN_VOLUME="dest/in_volume.nii.gz"
  BET_INPUT_VOLUME="./T1w_norm.nii.gz"
  MASK_VOLUME="./T1w_norm_noskull_mask.nii.gz"


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
