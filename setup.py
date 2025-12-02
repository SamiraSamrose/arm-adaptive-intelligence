from setuptools import setup, find_packages

setup(
    name="arm-adaptive-intelligence",
    version="1.0.0",
    description="ARM Adaptive Intelligence Engine for Edge AI",
    author="ARM AI Development Team",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "torch>=2.0.0",
        "tensorflow>=2.13.0",
        "onnx>=1.14.0",
        "onnxruntime>=1.15.0",
        "transformers>=4.30.0",
        "peft>=0.4.0",
        "bitsandbytes>=0.41.0",
        "chromadb>=0.4.0",
        "sentence-transformers>=2.2.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)