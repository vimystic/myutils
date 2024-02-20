def get_unique_noble_addresses(input_file, output_file):
    unique_addresses = set()

    # Open the input file and read line by line
    with open(input_file, 'r') as f:
        for line in f:
            # Extract the noble address from each line
            noble_address = line.split()[-1]
            # Add the noble address to the set
            unique_addresses.add(noble_address)

    # Write unique addresses to the output file
    with open(output_file, 'w') as f:
        for address in unique_addresses:
            f.write(address + '\n')

    print(f"Unique noble addresses written to {output_file}")


# Provide the input and output file paths
input_file = "txAndSrc.txt"
output_file = "unique.txt"

# Call the function to get unique noble addresses
get_unique_noble_addresses(input_file, output_file)
