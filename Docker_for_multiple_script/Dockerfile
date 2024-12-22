FROM jupyter/base-notebook:latest

# Install Papermill and any other Python packages needed
RUN pip install papermill schedule

# Copy the notebooks and scripts into the container
COPY notebooks /home/jovyan/work/notebooks
COPY execute_notebooks.py /home/jovyan/work/execute_notebooks.py  

# Set the working directory
WORKDIR /home/jovyan/work

# Command to run the execute_notebooks.py script
CMD ["python", "/home/jovyan/work/execute_notebooks.py"]
