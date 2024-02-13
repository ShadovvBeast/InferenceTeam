FROM nvidia/cuda:12.3.0-devel-ubuntu22.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y wget supervisor git cmake python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/ggerganov/llama.cpp.git /root/llama.cpp && \
    cd /root/llama.cpp && \
    git checkout 2891c8aa9af17f4ff636ff3868bc34ff72b56e25 && \
    mkdir build && \
    cd build && \
    cmake .. -DLLAMA_CUBLAS=ON && \
    cmake --build . --config Release && \
    cd ../models && \
    wget https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-dpo-GGUF/resolve/main/dolphin-2.6-mistral-7b-dpo.Q5_K_S.gguf
COPY inferenceteam.conf /etc/supervisor/conf.d/
COPY main.py /root/main.py
COPY .env /root/.env
COPY requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt

EXPOSE 8080

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]