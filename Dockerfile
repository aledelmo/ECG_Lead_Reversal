FROM tensorflow/tensorflow:latest-gpu-jupyter
LABEL maintainer="Alessandro Delmonte <delmonte.ale92@gmail.com>"

RUN echo -e "Acquire {http::proxy \"http://10.143.11.22:3128\"; https::proxy \"http://10.143.11.22:3128\";}" >> /etc/apt/apt.conf
RUN cat /etc/apt/apt.conf
RUN export {http_proxy,https_proxy,ftp_proxy}="http://10.143.11.22:3128/"
#RUN apt-get -y --fix-missing update & apt-get install -y python-opencv

## tcmalloc for memory leakage
# RUN apt install libtcmalloc-minimal4
# ENV LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4"

COPY requirements.txt /tf

#RUN pip uninstall -q -y tensorboard
#RUN pip install -q -U tb-nightly tensorboard_plugin_profile

WORKDIR /tf
RUN pip install --default-timeout=1000 --proxy=http://10.143.11.22:3128 -U -r  requirements.txt

EXPOSE 8888
EXPOSE 6006

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --debug --notebook-dir=/tf --ip 0.0.0.0 --allow-root"]

# docker build --build-arg https_proxy=https://10.143.11.22:3128 -f Dockerfile --rm --tag cardio .

# docker run -u $(id -u) --gpus all -it -v /home/imag2/External_Projects/Cardiologs:/tf --env HTTPS_PROXY=https://10.143.11.22:3128
# -p 8888:8888 -p 6006:6006 --rm --name ca cardio:latest
