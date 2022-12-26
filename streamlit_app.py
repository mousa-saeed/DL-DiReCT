import streamlit as st
import subprocess
import time
import sys
import os
log = subprocess.Popen([f'{sys.executable} -m pip install -e .'], stdout = subprocess.PIPE, stderr= subprocess.PIPE, shell=True)
  # wait for subprocess to install package before running your actual code below
# time.sleep(90)



st.write(os.getcwd())

st.write(print(log) )
st.file_uploader("File")
# st.write('## Run Streamlit on Colab with `pyngrok` ')
# st.write("This is an amazing tutorial, I love this channel!!!")
st.markdown("# maybe it worked")
st.write(os.listdir())
