import streamlit as st
import subprocess
import time
import sys
import os
log = subprocess.Popen([f'{sys.executable} -m pip install -e .'], stdout = subprocess.PIPE, stderr= subprocess.PIPE, shell=True)
  # wait for subprocess to install package before running your actual code below
# time.sleep(90)



st.write(os.getcwd())


st.write(subprocess.Popen(["dl+direct", "--subject", "001", "--lowmem", "--bet", "/content/drive/MyDrive/Hipposeg/patient_data/80100000_t1w_3d_tfe_nyul.nii.gz"], stdout = subprocess.PIPE, stderr= subprocess.PIPE, shell=True))

st.write(print(log) )
uploaded_file = st.file_uploader("Choose a file")
print(uploaded_file)


with open(os.path.join(os.getcwd(),uploaded_file.name),"wb") as f:
         f.write(uploaded_file.getbuffer())

# st.write('## Run Streamlit on Colab with `pyngrok` ')
# st.write("This is an amazing tutorial, I love this channel!!!")
st.markdown("# maybe it worked")
st.write(os.listdir())

st.wrtite(subprocess.Popen(["dl_direct"], stdout = subprocess.PIPE, stderr= subprocess.PIPE, shell=True))
