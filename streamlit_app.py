import streamlit as st
#import nibabel as nib
import subprocess
import time
import sys
import os



st.write(subprocess.run(["pip install nibabel") ) 
# st.write(subprocess.run([ "pip install -e ."], stdout = subprocess.PIPE, stderr= subprocess.PIPE, shell=True))
  # wait for subprocess to install package before running your actual code below
# time.sleep(90)



st.write(os.getcwd())


uploaded_file = st.file_uploader("Choose a file")
print(uploaded_file)


with open(os.path.join(os.getcwd(),uploaded_file.name),"wb") as f:
         f.write(uploaded_file.getbuffer())

# st.write('## Run Streamlit on Colab with `pyngrok` ')
# st.write("This is an amazing tutorial, I love this channel!!!")

st.write(subprocess.run(["python src/conform.py 80100000_t1w_3d_tfe_nyul.nii.gz T1w_norm.nii.gz "],  stdout = subprocess.PIPE, stderr= subprocess.PIPE, shell=True) )
# st.write(subprocess.run(["dl+direct", "--subject", "001", "--lowmem", "--bet", "/content/drive/MyDrive/Hipposeg/patient_data/80100000_t1w_3d_tfe_nyul.nii.gz"], stdout = subprocess.PIPE, stderr= subprocess.PIPE, shell=True))

st.markdown("# maybe it worked")
st.write(os.listdir())

# st.write(subprocess.run(["dl_direct"], stdout = subprocess.PIPE, stderr= subprocess.PIPE, shell=True))
