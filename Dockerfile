FROM ghcr.io/ggerganov/llama.cpp:full-cuda
RUN apt-get update && apt-get install -y wget
RUN cd models && wget https://huggingface.co/TheBloke/OpenHermes-2-Mistral-7B-GGUF/resolve/main/openhermes-2-mistral-7b.Q5_K_M.gguf
CMD ["--server", "-m", "/models/openhermes-2-mistral-7b.Q5_K_M.gguf", "--n-gpu-layers", "35", "--ctx-size", "4096"]