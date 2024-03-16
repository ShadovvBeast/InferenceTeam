FROM nvidia/cuda:12.3.0-devel-ubuntu22.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y wget supervisor git cmake python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/ggerganov/llama.cpp.git /root/llama.cpp && \
    cd /root/llama.cpp && \
    git checkout ceca1aef0738b57951cd12c603c3477e75312dec && \
    mkdir build && \
    cd build && \
    cmake .. -DLLAMA_CUBLAS=ON && \
    cmake --build . --config Release && \
    cd ../models && \
    wget https://huggingface.co/ShadowBeast/llava-v1.6-mistral-7b-Q5_K_S-GGUF/resolve/main/llava-v1.6-mistral-7b-Q5_K_S.gguf && \
    wget https://huggingface.co/ShadowBeast/llava-v1.6-mistral-7b-Q5_K_S-GGUF/resolve/main/mmproj-model-f16.gguf
COPY inferenceteam.conf /etc/supervisor/conf.d/
COPY main.py /root/main.py
COPY .env /root/.env
COPY requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt

EXPOSE 8080

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]