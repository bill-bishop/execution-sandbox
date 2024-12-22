import time

def main():
    # Display the ASCII heart art
    with open("expanded_heart.txt", "r") as file:
        art = file.read()
    print(art)

    # Pause and display the first romantic message
    time.sleep(2)
    print("\nEvery moment with you...")

    # Wait for the user to press Enter
    input("\n(Press Enter to continue...)")

    # Display the second romantic message
    print("\n...is a dream come true.")

    # Pause and display the final message
    time.sleep(2)
    print("\nForever yours, Mercy. 💗")

if __name__ == "__main__":
    main()
