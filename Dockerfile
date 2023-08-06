# First, we will use the nvidia cuda image
FROM nvidia/cuda:10.2-base
CMD nvidia-smi

# On top of it we also use our ubuntu 22.04 image
FROM ubuntu:22.04

# Next, we will define the maintainer of our image and its email
LABEL maintainer="Carlos Gonzalez" email="cgonv1993@gmail.com"

# We make our image non-interactive
ENV DEBIAN_FRONTEND noninteractive

# We update the whole system
RUN apt-get -y update && apt-get -y upgrade

# Install basics
RUN apt install -y \
git \
nano \
wget \
curl \
zip \
fim \
mplayer \
python3-pip \
xfce4-terminal \
terminator \
libgl1-mesa-dev \
libxcb-* \
libxkb*

# Install jupyter
RUN python3 -m pip install jupyterlab

# Install Mask-RCNN-pytorch dependencies
RUN pip install \
pycocotools \
opencv-python-headless \
tqdm \
ffmpeg

# Install torch and compatible torchvision and torchaudio (it has to be torch version lower than 2.0) for Mask-RCNN-pytorch
RUN pip install \
torch==1.13.1 \
torchvision==0.14.1 \
torchaudio==0.13.1

# Install dependencies for labelme
RUN pip install --upgrade / 
imgviz /
labelme

# # Install requirements for labelme
# RUN apt-get install -y labelme

# Go to /myyolov7 folder
WORKDIR /docker-mask-rcnn-pytorch

# Copy labelme from directory to container
COPY labelme labelme

# Copy Mask-RCNN-pytorch from directory to container
COPY Mask-RCNN-pytorch Mask-RCNN-pytorch

# Copy Python file for applying data augmentation to images
COPY data_augmentation.py data_augmentation.py

# Copy executable bash script for split data, organize images and labels in subfolders and create training yaml files:
COPY preparation_for_training preparation_for_training

# OPTIONAL: Copy images folder (make sure you have your images that you will annotate on it) from directory to container
COPY images images

# Set the default command to start terminator
CMD ["terminator"]