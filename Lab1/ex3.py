from ex2 import shift

filein = "flag"

for i in range(0, 256):
    shift(filein, f"out/{i}.txt", i * -1)

# then run `file *` in the out directory and flag any discrepancies
# key is 246, an image of the Swiss flag