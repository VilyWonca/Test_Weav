import os

os.environ["NO_PROXY"] = "localhost,127.0.0.1"

import ollama

embed = ollama.embed(model='nomic-embed-text:latest', input='The sky is blue because of rayleigh scattering')

print(embed)