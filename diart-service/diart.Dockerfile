# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app/
COPY . .

# Create the conda environment from the environment.yml file
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "diart", "/bin/bash", "-c"]


# Ensure the environment is activated
RUN echo "conda activate diart" >> ~/.bashrc


# Set the default command to execute the script when the container starts
CMD ["conda", "run", "--no-capture-output", "-n", "diart", "python", "app.py"]
