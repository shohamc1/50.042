from gf2n import *

add_matrix = []
mul_matrix = []
ip_4 = Polynomial2([1, 0, 0, 1, 1])

for i in range(16):
    current_poly_row = i
    row_candidate = GF2N(current_poly_row, 4, ip_4)
    add_list = []
    for j in range(16):
        current_poly_col = j
        col_candidate = GF2N(current_poly_col, 4, ip_4)
        add_list.append(col_candidate.add(row_candidate).getInt())
    add_matrix.append(add_list)

for i in range(15):
    current_poly_row = i + 1
    row_candidate = GF2N(current_poly_row, 4, ip_4)
    add_list = []
    mul_list = []
    for j in range(15):
        current_poly_col = j + 1
        col_candidate = GF2N(current_poly_col, 4, ip_4)
        mul_list.append(col_candidate.mul(row_candidate).getInt())
    mul_matrix.append(mul_list)

ip = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
s_box_matrix = []
for i in range(16):
    x_row = i
    row_list = []
    for j in range(16):
        y_col = j
        int_value = int(16 * x_row + y_col)
        current_candidate = GF2N(int_value, 8, ip)
        affined_candidate = current_candidate.mulInv().affineMap()
        row_list.append(hex(affined_candidate.getInt()))
    s_box_matrix.append(row_list)


# addition table
print("-- ADDITION TABLE --")
for j in add_matrix:
    for i in j:
        print("{:2}".format(str(i)), end=" ")
    print()

print("\n\n")

# multiplication table
print("-- MULTIPLICATION TABLE --")
for j in mul_matrix:
    for i in j:
        print("{:2}".format(str(i)), end=" ")
    print()

print("\n\n")

# s box
print("-- S BOX MATRIX --")
for j in s_box_matrix:
    for i in j:
        print("{:4}".format(str(i)), end=" ")
    print()
