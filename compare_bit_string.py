# Define the input binary strings
binary_str1 = "0010101100110000001100000011000000110000001000000011000100010001000000000000000010000000000000000000110100001010"
binary_str2 = "0010101100110000001100000011000000110000001000000011000100010001000001000000000010000000000000000000110100001010"

# Convert the binary strings into a single binary sequence (without spaces)
sequence1 = ''.join(binary_str1.split())
sequence2 = ''.join(binary_str2.split())

# Ensure the sequences are of the same length
if len(sequence1) != len(sequence2):
    print("The binary sequences must have the same length.")
else:
    # Compare bit-by-bit and find positions of differing bits
    differing_bits = [index for index, (bit1, bit2) in enumerate(zip(sequence1, sequence2)) if bit1 != bit2]

    # Display results
    if differing_bits:
        print("Differing bit positions:", differing_bits)
    else:
        print("The binary sequences are identical.")
