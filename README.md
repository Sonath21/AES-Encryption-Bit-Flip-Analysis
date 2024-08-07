# AES-Encryption-Bit-Flip-Analysis

## Overview
This project provides a Python implementation to analyze the impact of bit flips on AES-encrypted messages. It supports encryption using AES in both ECB and CBC modes, introduces random bit flips in the messages, and calculates the Hamming distances between the original and flipped encrypted messages to study the sensitivity and robustness of these encryption modes against bit manipulation.

## Features
- **AES Encryption**: 
  - Supports both ECB (Electronic Codebook) and CBC (Cipher Block Chaining) modes.
  - Utilizes the PyCryptodome library for robust and secure encryption.
- **Bit Flipping**: 
  - Randomly flips a single bit in the message to simulate bit errors or intentional bit manipulation.
- **Hamming Distance Calculation**: 
  - Measures the number of differing bits between the original and modified ciphertexts, providing insight into the diffusion properties of the encryption modes.

## Getting Started

### Prerequisites
- Python 3.x
- NumPy
- PyCryptodome

### Installation
Install the required packages using pip:
```bash
pip install numpy pycryptodome
