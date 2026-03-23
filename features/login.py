def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        with open("users.txt", "r") as file:
            users = file.readlines()
    except FileNotFoundError:
        print("No users found. Please register first.")
        return

    for user in users:
        saved_username, saved_password = user.strip().split(",")

        if username == saved_username and password == saved_password:
            print("Login successful ✅")
            return

    print("Invalid username or password ❌")


if __name__ == "__main__":
    login()