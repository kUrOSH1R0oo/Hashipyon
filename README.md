![GIF](https://github.com/kUrOSH1R0oo/Hashipyon/blob/main/despair.gif)

# Hashipyon

Hashipyon is a high-performance Argon2 hash cracker that uses a dictionary-based attack to recover plaintext passwords. It supports Argon2i, Argon2d, and Argon2id variants, providing flexibility in handling different Argon2 hashes.

---

## About Argon2

**Argon2** is a modern password hashing algorithm designed to be secure against both GPU and ASIC attacks by consuming substantial memory and computation time. It won the Password Hashing Competition (PHC) in 2015 and has become a widely accepted standard for password security.

### Argon2 Variants:
- **Argon2i**: Optimized against side-channel attacks, using data-independent memory access.  
- **Argon2d**: Optimized for resistance against GPU cracking, using data-dependent memory access.  
- **Argon2id**: A hybrid combining Argon2i and Argon2d for balanced security.  

### How Argon2 Works:
1. **Salt Generation**: A random salt is generated and combined with the password.  
2. **Memory Filling**: It uses memory blocks in a complex sequence to slow down brute-force attacks.  
3. **Iterations**: Adjustable time and memory cost factors increase hash complexity.  
4. **Final Hash**: The result is a unique, hardened hash that is hard to reverse.  

---

## Hashipyon's Features

- Multi-threaded for enhanced speed.  
- Supports Argon2i, Argon2d, and Argon2id hash variants.  
- Real-time progress display with attempts, speed, and ETA.  
- Saves cracked passwords to a specified output file (If specified).

---

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/kUrOSH1R0oo/Hashipyon
    ``` 
2. **Run the Installer Script**
    ```bash
    sudo ./install.sh
    ```
3. **After Installation, just type 'hashipyon' in command-line for usage**
    ```bash
    hashipyon
    ```

---

## Basic Usage

```bash
hashipyon <argon2_hash> -w <path-to-wordlist> -t <num_threads>
```

---

## License

- Hashipyon is licensed under MIT License.

---

## Warning

- This tool is strictly intended for **educational and research purposes only**. Its primary objective is to demonstrate how the Argon2 hashing algorithm can be analyzed and potentially cracked in controlled, ethical environments. **Unauthorized or malicious use of this tool against systems, networks, or data without explicit permission is illegal and unethical.** The developer holds no responsibility for any misuse or damage caused by this tool. Always ensure your actions comply with local laws and cybersecurity regulations. Use responsibly and ethically.

---

## Author

- KuroShiro (A1SBERG)

