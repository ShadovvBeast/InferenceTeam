FROM nvidia/cuda:12.3.0-devel-ubuntu22.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y wget supervisor git cmake python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/ggerganov/llama.cpp.git /root/llama.cpp && \
    cd /root/llama.cpp && \
    git checkout 2833a6f63c1b87c7f4ac574bcf7a15a2f3bf3ede && \
    mkdir build && \
    cd build && \
    cmake .. -DLLAMA_CUBLAS=ON && \
    cmake --build . --config Release && \
    cd ../models && \
    wget https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF/resolve/main/openhermes-2.5-mistral-7b.Q5_K_M.gguf
COPY inferenceteam.conf /etc/supervisor/conf.d/
COPY main.py /root/main.py
COPY .env /root/.env
COPY requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]