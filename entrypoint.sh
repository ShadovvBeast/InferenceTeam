#!/bin/bash

# First, run the NVIDIA entrypoint
/opt/nvidia/nvidia_entrypoint.sh

# Then, run supervisord
exec /usr/bin/supervisord -n
