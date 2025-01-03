import math

space_m = 32
m = 31

space_H0 = math.log2(space_m)
H0 = math.log2(m)

H_space_mono = 4.352755973064407
H_space_bi_o = 3.954954429877953
H_space_bi = 3.9551987303678136

H_mono = 4.4529625721687855
H_bi_o = 4.130036128201785
H_bi = 4.127746677871504

print("R_space_mono:", 1 - H_space_mono/space_H0)
print("R_space_bi_o:", 1 - H_space_bi_o/space_H0)
print("R_space_bi:", 1 - H_space_bi/space_H0)

print("R_mono:", 1 - H_mono/H0)
print("R_bi_o:", 1 - H_bi_o/H0)
print("R_bi:", 1 - H_bi/H0)

