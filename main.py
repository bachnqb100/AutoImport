# Open the file in read mode
with open('E:/Python/AutoImport/inputVoucherTest', 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Process the line here
        print(line.strip())  # This will print each line without trailing newline characters
