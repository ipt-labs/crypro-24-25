import math

FILENAME_WITH_WHITESPACES = "./seneka.txt"
FILENAME_WITHOUT_WHITESPACES = "./seneka_no_whitespace.txt"
ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def prepare_text(text, with_space=False):
    if with_space==True:
        text_filtered = ''.join([char.lower() for char in text if char.lower() in (ALPHABET+' ')])
        text_filtered = ' '.join(text_filtered.split())
    else:
        text_filtered = ''.join([char.lower() for char in text if char.lower() in ALPHABET])
        text_filtered = ' '.join(text_filtered.split())
    return text_filtered

def calculate_monogram_frequencies(text_filtered):
    mono_freq_percentage = {}
    mono_freq_counter = {}
    mono_counter = 0
    for i in range(0, len(text_filtered), 1):
        monogram = text_filtered[i:i+1]
        mono_counter += 1
        if monogram in mono_freq_counter:
            mono_freq_counter[monogram] += 1
        else:
            mono_freq_counter[monogram] = 1

    for monogram, freq in mono_freq_counter.items():
        mono_freq_percentage[monogram] = freq/mono_counter

    return mono_freq_percentage

def calculate_monogram_entropy(mono_freq_percentage):
    mono_entropy = 0
    for freq in mono_freq_percentage.values():
        if not freq:
            continue
        mono_entropy += (math.log2(freq))*freq
    mono_entropy = (-1) * mono_entropy
    return mono_entropy

def calculate_monogram_redundancy(mono_entropy):
    mono_redundancy = 1-(mono_entropy / math.log2(len(ALPHABET)))
    return mono_redundancy

def calculate_bigram_frequencies(text_filtered, step):
    bi_freq_percentage = {}
    bi_freq_counter = {}
    bi_counter = 0
    for i in range(0, len(text_filtered)-1, step):
        bigram = text_filtered[i:i+2]
        bi_counter += 1
        if bigram in bi_freq_counter:
            bi_freq_counter[bigram] += 1
        else:
            bi_freq_counter[bigram] = 1

    for bigram, freq in bi_freq_counter.items():
        bi_freq_percentage[bigram] = freq/bi_counter

    return bi_freq_percentage

def print_bigram_matrix(bi_freq_percentage, with_space=False):
    # Create an alphabet list for matrix indexing
    alphabet = ALPHABET
    if with_space:
        alphabet = ALPHABET + ' '
    alphabet = list(alphabet)
    size = len(alphabet)
    
    # Create a matrix with zeros
    matrix = [[0.0 for _ in range(size)] for _ in range(size)]

    # Populate the matrix with bigram frequencies (multiplied by 100)
    for bigram, freq in bi_freq_percentage.items():
        if len(bigram) == 2:
            row = alphabet.index(bigram[0])
            col = alphabet.index(bigram[1])
            matrix[row][col] = round(freq * 100, 3)  # Multiply by 100 and reduce to 3 decimal places

    # Adjust column width for alignment
    column_width = max(len(char) for char in alphabet) + 5  # Adjust the width of each column

    # Print header row (alphabet letters)
    header = " ".join(f"{char:>{column_width}}" for char in alphabet)
    print(f"{'':>{column_width}} {header}")  # Add padding for the first column

    # Print each row with corresponding bigram frequencies
    for i, row in enumerate(matrix):
        row_str = " ".join(f"{val:>{column_width}.3f}" for val in row)  # Format each number to 3 decimal places
        print(f"{alphabet[i]:>{column_width}} {row_str}")

def calculate_bigram_entropy(bi_freq_percentage):
    bi_entropy = 0
    for freq in bi_freq_percentage.values():
        if not freq:
            continue
        bi_entropy += (math.log2(freq))*freq
    bi_entropy = ((-1) * bi_entropy)/2
    return bi_entropy

def calculate_bigram_redundancy(bi_entropy):
    bi_redundancy = 1-(bi_entropy / math.log2(len(ALPHABET)))
    return bi_redundancy

def main():

    # working with file with whitespaces
    with open(FILENAME_WITH_WHITESPACES, 'r', encoding='utf-8') as file:
        text_with_whitespaces = file.read()
    
        # working with monograms
        text_with_whitespaces_filtered = prepare_text(text_with_whitespaces, with_space=True)
        mono_freq_percentage = calculate_monogram_frequencies(text_with_whitespaces_filtered)
        H1_mono_entropy = calculate_monogram_entropy(mono_freq_percentage)
        R1_mono_redundancy = calculate_monogram_redundancy(H1_mono_entropy)

        # working with bigrams with step 1
        bi_freq_percentage_step1 = calculate_bigram_frequencies(text_with_whitespaces_filtered, 1)
        H2_bi_entropy_step1 = calculate_bigram_entropy(bi_freq_percentage_step1)
        R2_bi_redundancy_step1 = calculate_bigram_redundancy(H2_bi_entropy_step1)

        # working with bigrams with step 2
        bi_freq_percentage_step2 = calculate_bigram_frequencies(text_with_whitespaces_filtered, 2)
        H2_bi_entropy_step2 = calculate_bigram_entropy(bi_freq_percentage_step2)
        R2_bi_redundancy_step2 = calculate_bigram_redundancy(H2_bi_entropy_step2)

        # printing required info
        print("\n^^^^ WORKING WITH FILE THAT HAS WHITESPACES ^^^^\n\n")

        # Printing monogram frequencies line by line
        print("Monogram frequencies:")
        for monogram, frequency in mono_freq_percentage.items():
            print(f"{monogram}: {frequency}")

        print(f"\nMonogram's entropy: {H1_mono_entropy}\n")
        print(f"Monogram's redundancy: {R1_mono_redundancy}\n")

        print("\nSTEP ONE Bigram's matrix:")
        print_bigram_matrix(bi_freq_percentage_step1, with_space=True)

        print(f"\nSTEP ONE Bigram's entropy: {H2_bi_entropy_step1}\n")
        print(f"STEP ONE Bigram's redundancy: {R2_bi_redundancy_step1}\n")

        print("\nSTEP TWO Bigram's matrix:")
        print_bigram_matrix(bi_freq_percentage_step2, with_space=True)

        print(f"\nSTEP TWO Bigram's entropy: {H2_bi_entropy_step2}\n")
        print(f"STEP TWO Bigram's redundancy: {R2_bi_redundancy_step2}\n")
        print("-"*60)

    # working with file withOUT whitespaces
    with open(FILENAME_WITHOUT_WHITESPACES, 'r', encoding='utf-8') as file:
        text_without_whitespaces = file.read()
    
        # working with monograms
        text_without_whitespaces_filtered = prepare_text(text_without_whitespaces)
        mono_freq_percentage = calculate_monogram_frequencies(text_without_whitespaces_filtered)
        H1_mono_entropy = calculate_monogram_entropy(mono_freq_percentage)
        R1_mono_redundancy = calculate_monogram_redundancy(H1_mono_entropy)

        # working with bigrams with step 1
        bi_freq_percentage_step1 = calculate_bigram_frequencies(text_without_whitespaces_filtered, 1)
        H2_bi_entropy_step1 = calculate_bigram_entropy(bi_freq_percentage_step1)
        R2_bi_redundancy_step1 = calculate_bigram_redundancy(H2_bi_entropy_step1)

        # working with bigrams with step 2
        bi_freq_percentage_step2 = calculate_bigram_frequencies(text_without_whitespaces_filtered, 2)
        H2_bi_entropy_step2 = calculate_bigram_entropy(bi_freq_percentage_step2)
        R2_bi_redundancy_step2 = calculate_bigram_redundancy(H2_bi_entropy_step2)

        # printing required info
        print("\n^^^^ WORKING WITH FILE THAT HAS >NOT< WHITESPACES ^^^^\n\n")

        # Printing monogram frequencies line by line
        print("Monogram frequencies (without whitespaces):")
        for monogram, frequency in mono_freq_percentage.items():
            print(f"{monogram}: {frequency}")

        print(f"\nMonogram's entropy: {H1_mono_entropy}\n")
        print(f"Monogram's redundancy: {R1_mono_redundancy}\n")

        print("\nSTEP ONE Bigram's matrix:")
        print_bigram_matrix(bi_freq_percentage_step1)

        print(f"\nSTEP ONE Bigram's entropy: {H2_bi_entropy_step1}\n")
        print(f"STEP ONE Bigram's redundancy: {R2_bi_redundancy_step1}\n")

        print("\nSTEP TWO Bigram's matrix:")
        print_bigram_matrix(bi_freq_percentage_step2)

        print(f"\nSTEP TWO Bigram's entropy: {H2_bi_entropy_step2}\n")
        print(f"STEP TWO Bigram's redundancy: {R2_bi_redundancy_step2}\n")

    return

if __name__ == "__main__":
    main()