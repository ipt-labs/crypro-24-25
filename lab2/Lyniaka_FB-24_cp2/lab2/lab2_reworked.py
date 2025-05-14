import matplotlib.pyplot as plt

from text_source_plus import TextSourcePlus
from alphabet import Alphabet
from vizhener_decipher import VizhenerDecipher, index_of_coincidence, cipher_source

PATH_LAB1 = "..\\lab1\\"
LONG_FILE_NAME = "rus_text.txt"
PATH_LAB2 = "..\\lab2\\"
SHORT_FILE_NAME = "short_rus_text.txt"
CIPHERED_FILE_NAME = "ciphered.txt"

RUS_LOWERCASE_WITH_HARD = "абвгдежзийклмнопрстуфхцчшщъыьэюя"


def frequencies_numbers_gen(r, alphabet: Alphabet):
    k = 0
    while True:
        frequencies_numbers = [k] * r
        yield frequencies_numbers
        k = (k + 1) % alphabet.m


def decipher(v_d: VizhenerDecipher, alphabet: Alphabet, language_source: TextSourcePlus):
    period = v_d.detect_key_period()
    if period:
        print(f"Detected period: {period}")
    else:
        print("Can't detect key period")
        return

    gen = frequencies_numbers_gen(period, alphabet)
    keyword = ""
    while True:
        if not keyword:
            frequiencies_numbers = next(gen)
        keyword, open_list = v_d.decipher(period, language_source, keyword, frequiencies_numbers)
        print(f"keyword: {keyword}")
        print(f"Decipered text: {open_list}")
        to_continue = input("Continue deciphering? [y/n] ")
        if to_continue.lower() != 'y':
            break

        keyword = input(f"Enter keyword ({period} characters) "
                        "or <Enter> to automatically generate keyword: ")
    return keyword, ''.join(open_list)


def plot_bar(x, y, xlabel, ylabel, title, color='b'):
    plt.rcParams["figure.figsize"] = (12, 5)
    plt.bar(x, y, width=0.8, color=color)
    plt.xticks(x)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


alphabet = Alphabet(RUS_LOWERCASE_WITH_HARD)
long_source = TextSourcePlus(PATH_LAB1 + LONG_FILE_NAME, alphabet, "to_lower", "replace_ru_yo",
                             "delete_delimeters", "delete_spaces")
long_source.apply_filter_chain()
rus_index_of_coincidence = index_of_coincidence(long_source)
print(f"rus_index_of_coincidence {rus_index_of_coincidence}")

key_len = int(input("Key len: "))

short_source = TextSourcePlus(PATH_LAB2 + SHORT_FILE_NAME, alphabet, "to_lower", "replace_ru_yo",
                              "delete_delimeters", "delete_spaces")
short_source.apply_filter_chain()
short_index = index_of_coincidence(short_source)
print(f"Open text index of coincidence {short_index}")

keywords, ciphered_dict = cipher_source(short_source, 2, 30)
print(f"keywords {keywords}")
print(f"ciphered text for key len {key_len} : {ciphered_dict[key_len]}")
print("Ciphered texts indexes of coincidence")
for r, ciphered in ciphered_dict.items():
    ciph_source = TextSourcePlus.from_string(ciphered, alphabet)
    ciph_source.apply_filter_chain()
    ciphered_ind = index_of_coincidence(ciph_source)
    print(f" {r}  {ciphered_ind}")

v_d = VizhenerDecipher(TextSourcePlus.from_string(ciphered_dict[key_len], alphabet),
                       rus_index_of_coincidence)
print("\nperiodic_method1_period_finder")
periodic_ids_list = v_d.periodic_method1_period_finder(return_all=True)
print("period   index of coincidence")
x = []
y = []
for r, id_of_coid, _, _ in periodic_ids_list:
    print(f"{r:5}     {id_of_coid:6.4f}")
    x.append(r)
    y.append(id_of_coid)
plot_bar(x, y, "period", "index of coincidence", "indexes of coincidence for different periods")

print("non_periodic_method1_period_finder")
print(v_d.non_periodic_method1_period_finder(ciphered_dict))

print("\nstat_equals_method2_period_finder")
stats_dict = v_d.stat_equals_method2_period_finder(return_all=True)
print("period   equals stats")
x = []
y = []
for r, stat_eq in stats_dict.items():
    print(f"{r:5}     {stat_eq:6}")
    x.append(r)
    y.append(stat_eq)
plot_bar(x, y, "period", "stats value", "Stats values (D) for different periods", color='g')

print("detect_key_period")
period = v_d.detect_key_period()
if period:
    print(period)
else:
    print("Can't detect key period")

print("\nDeciphering ciphered text (variant 10)")
ciphered_source = TextSourcePlus(PATH_LAB2 + CIPHERED_FILE_NAME, alphabet)
v_d = VizhenerDecipher(ciphered_source, rus_index_of_coincidence)
keyword, open_text = decipher(v_d, alphabet, long_source)

line_len = 60
print(f"\nIn the end of deciphering keyword is: {keyword}")
print("Open text is:")
for i in range(0, len(open_text), line_len):
    print(open_text[i: i + line_len])
