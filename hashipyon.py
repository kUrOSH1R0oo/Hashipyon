#!/usr/bin/env python3 
import concurrent.futures
import os
import optparse
from argon2 import PasswordHasher, exceptions
import sys
import time
import threading

banner = r"""
                 _     _
  /\  /\__ _ ___| |__ (_)_ __  _   _  ___  _ __
 / /_/ / _` / __| '_ \| | '_ \| | | |/ _ \| '_ \
/ __  / (_| \__ \ | | | | |_) | |_| | (_) | | | |
\/ /_/ \__,_|___/_| |_|_| .__/ \__, |\___/|_| |_|
                        |_|    |___/ ~ A1SBERG
"""

attempts = 0
start_time = time.time()
lock = threading.Lock()

def get_variant_from_hash(hash):
    if '$argon2i$' in hash:
        return 'argon2i'
    elif '$argon2d$' in hash:
        return 'argon2d'
    elif '$argon2id$' in hash:
        return 'argon2id'
    else:
        return 'unknown'

def update_progress(variant):
    global attempts, start_time
    while True:
        with lock:
            elapsed_time = time.time() - start_time
            attempts_per_sec = attempts / elapsed_time if elapsed_time > 0 else 0
            remaining_attempts = total_word_count - attempts
            eta = remaining_attempts / attempts_per_sec if attempts_per_sec > 0 else 0
            sys.stdout.write(f"\r[*] Cracking {variant}... | Attempts: {attempts} | Speed: {attempts_per_sec:.2f}/s | ETA: {eta:.2f}s")
            sys.stdout.flush()
        time.sleep(0.5)

def validate_password(candidate):
    global attempts
    try:
        if password_hasher.verify(target_hash, candidate):
            with lock:
                print("\n" + "-" * 60)
                print(f"[+] Found!")
                print(f"[+] Plaintext: {candidate}")
                if options.output:
                    with open(options.output, 'w') as file:
                        file.write(f"{target_hash} -> {candidate}\n")
                os._exit(0)
    except exceptions.VerifyMismatchError:
        pass
    except exceptions.InvalidHash:
        with lock:
            print("[!] Invalid Argon2 hash format.")
            os._exit(1)
    except Exception as e:
        with lock:
            print(f"[!] Error during validation: {e}")
    finally:
        with lock:
            attempts += 1

def calculate_wordlist_size(wordlist_path):
    try:
        with open(wordlist_path, 'r', encoding='Latin-1') as file:
            return sum(1 for line in file)
    except FileNotFoundError:
        print(f"[!] Wordlist file not found: {wordlist_path}")
        sys.exit(1)
    except Exception:
        print(f"[!] No wordlist provided. Nothing to compare.")
        sys.exit(1)

if __name__ == '__main__':
    parser = optparse.OptionParser(
    description="""Hashipyon attempts to crack Argon2 password hashes using a dictionary-based attack. It leverages multi-threading to speed up the process by checking potential passwords from a given wordlist. The hash is validated using the Argon2 password hashing algorithm, and Hashipyon supports Argon2i, Argon2d, and Argon2id Variants. Argon2 is designed to be memory-intensive and time-costly to defend against brute-force attacks, making it one of the most secure password hashing algorithms available today. Hashipyon uses a dictionary-based attack by comparing each password from the provided wordlist to the Argon2 hash using the embedded salt.
    Note: The cracking process depends on the strength of the hash, the memory cost, and the time cost set during the hash creation. Strong Argon2 hashes with high cost factors (memory/time) may take a significant amount of time to crack, even with a large wordlist.
    """
    )
    parser.add_option('-w', '--wordlist', dest="wordlist", help="Path to wordlist")
    parser.add_option('-t', '--threads', dest="threads", type=int, help="Number of threads")
    parser.add_option('-o', '--output', dest="output", help="File to save cracked password")
    options, args = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)

    target_hash = args[0]
    wordlist_path = options.wordlist
    num_threads = options.threads if options.threads else 4

    if num_threads <= 0:
        print("[!] Number of threads must be a positive integer.")
        sys.exit(1)

    variant = get_variant_from_hash(target_hash)
    os.system('clear')
    print(banner)
    print(f"[+] Hash: {target_hash}")
    print(f"[+] Wordlist: {wordlist_path}")
    print(f"[+] Threads: {num_threads}")

    if options.output:
        print(f"[+] Output File: {options.output}")

    try:
        password_hasher = PasswordHasher()
        total_word_count = calculate_wordlist_size(wordlist_path)
    except Exception as e:
        print(f"[!] Error initializing hasher or wordlist: {e}")
        sys.exit(1)

    progress_thread = threading.Thread(target=update_progress, args=(variant,))
    progress_thread.daemon = True
    progress_thread.start()

    try:
        with open(wordlist_path, 'r', encoding='Latin-1') as wordlist:
            words = wordlist.read().splitlines()
    except Exception as e:
        print(f"[!] Failed to load wordlist: {e}")
        sys.exit(1)

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(validate_password, words)
    except Exception as e:
        print(f"[!] Error during cracking process: {e}")
        sys.exit(1)
    progress_thread.join()
    print("\n[+] Cracking completed.")

