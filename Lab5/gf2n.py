# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2021

from typing import List
import copy


class Polynomial2:
    def __init__(self, coeffs: List[int]):
        self.co = coeffs

    def add(self, p2: List[int]):
        first = copy.deepcopy(self.co)
        second = copy.deepcopy(p2.co)

        if len(first) != len(second):
            diff = abs((len(first) - len(second)))

            if len(second) < len(first):
                for _ in range(diff):
                    second.append(0)
            else:
                for _ in range(diff):
                    first.append(0)

        res: List[int] = []

        for i, j in zip(first, second):
            res.append(i ^ j)

        return Polynomial2(res)

    def sub(self, p2: List[int]):
        return self.add(p2)  # they are the same operation

    def mul(self, p2: List[int], modp=None):
        iteration_number = self.degree() + 1
        multiplier = copy.deepcopy(p2.co)
        source = copy.deepcopy(self.co)

        if modp:
            modp_array: List[int] = copy.deepcopy(modp.co)
            length_difference = len(modp_array) - len(multiplier)
            multiplier.extend([0] * (length_difference - 1))
            res = []

            for i in range(iteration_number):
                if i == 0:
                    continue
                elif multiplier[-1] == 0 and i == iteration_number - 2:
                    multiplier.insert(0, 0)
                    multiplier.pop()
                elif multiplier[-1] == 0:
                    multiplier.insert(0, 0)
                    multiplier.pop()
                elif multiplier[-1] == 1:
                    multiplier.insert(0, 0)

                    XOR: List[int] = []

                    for x, y in zip(multiplier, modp_array):
                        XOR.append(x ^ y)

                    XOR.pop()
                    multiplier = XOR
            if source[i] == 1:
                res.append(copy.deepcopy(multiplier))
        else:
            res = []
            multiplier.extend([0] * iteration_number)

            for i in range(iteration_number):
                if i != 0:
                    multiplier.insert(0, 0)
                    multiplier.pop()
                if source[i] == 1:
                    res.append(copy.deepcopy(multiplier))

        ret: List[int] = []

        for aligned_bits in zip(*res):
            temp = 0
            for bits in aligned_bits:
                temp = bits ^ temp

            ret.append(temp)

        return Polynomial2(ret)

    def div(self, p2: List[int]):
        q = Polynomial2([])
        r = Polynomial2(copy.deepcopy(self.co))

        d = p2.degree()
        c = p2.lc()

        while r.degree() >= d:
            if r.degree() == 0 and r.lc() == 0:
                break

            s_content = int(r.lc() / c)
            s_index = r.degree() - d

            temp = [0] * s_index
            temp.append(s_content)

            s = Polynomial2(temp)

            q = s.add(q)
            r = r.add(s.mul(p2))

        return q, r

    def __str__(self) -> str:
        res = ""

        for index, coeff in enumerate(self.co[::-1]):
            if coeff == 1:
                res += f"x^{len(self.co) - index - 1}+"

        return res.rstrip("+") or ""

    def getInt(p) -> int:
        index = 0
        sum = 0
        co = p.co

        for coeff in co:
            if coeff == 1:
                sum += coeff * (2 ** index)

            index += 1

        return sum

    def lc(self) -> int:
        coefficients = copy.deepcopy(self.co)
        # TODO: added this for aes
        if len(coefficients) == 0:
            return 0
        for i in range(len(coefficients)):
            highest_coeff = coefficients.pop()
            if highest_coeff == 1:
                return highest_coeff
        return 0

    def degree(self) -> int:
        co = copy.deepcopy(self.co)

        if len(co) == 0:
            return 0

        index = len(co) - 1

        for _ in range(index + 1):
            highest = co.pop()

            if highest == 1:
                return index

            index -= 1

        return 0


class GF2N:
    affinemat = [
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1],
    ]

    def __init__(self, x, n=8, ip=Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])):
        self.x = x
        self.n = n
        self.ip = ip
        self.p = self.getPolynomial2()

    def add(self, g2):
        copy_arr = copy.deepcopy(self.p.co)
        copy_poly = Polynomial2(copy_arr)

        res = copy_poly.add(g2.p)
        x = res.getInt()

        n = res.degree() + 1
        return GF2N(x, n, self.ip)

    def sub(self, g2):
        return self.add(self, g2)

    def mul(self, g2):
        copy_arr = copy.deepcopy(self.p.co)
        copy_poly = Polynomial2(copy_arr)

        res = copy_poly.mul(g2.p, self.ip)
        x = res.getInt()

        n = res.degree() + 1
        return GF2N(x, n, self.ip)

    def div(self, g2):
        copy_arr = copy.deepcopy(self.p.co)
        copy_poly = Polynomial2(copy_arr)

        quo, remainder = copy_poly.div(g2.p)

        x_r = remainder.getInt()
        x_q = quo.getInt()

        n_r = remainder.degree() + 1
        n_q = quo.degree() + 1

        r = GF2N(x_r, n_r, self.ip)
        q = GF2N(x_q, n_q, self.ip)

        return r, q

    def getPolynomial2(self):
        if self.x == 0:
            return Polynomial2([0])

        co = [1 if bit == "1" else 0 for bit in bin(self.x)[2:]]
        co.reverse()

        return Polynomial2(co)

    def __str__(self) -> str:
        return str(self.x)

    def getInt(self):
        return self.getPolynomial2().getInt()

    def mulInv(self):
        r1, r2 = self.ip, self.p
        t1, t2 = Polynomial2([0]), Polynomial2([1])

        while r2.getInt() > 0:
            quo, remainder = r1.div(r2)
            r = r1.sub(quo.mul(r2))
            r1, r2 = r2, r

            t = t1.sub(quo.mul(t2))
            t1, t2 = t2, t

        if r1.getInt() == 1:
            return GF2N(t1.getInt(), self.n, self.ip)
        if self.x == 0:
            return GF2N(0, self.n, self.ip)

    def affineMap(self):
        rhs = [1, 1, 0, 0, 0, 1, 1, 0]
        b_prime = self.getPolynomial2().co

        ret = []
        idx = 0

        for bit_array in self.affinemat:
            temp = []

            for x, y in zip(bit_array, b_prime):
                temp.append(x & y)

            res = 0

            for bit in temp:
                res = res ^ bit

            res = res ^ rhs[idx]
            ret.append(res)

            idx += 1

        return GF2N(Polynomial2(ret).getInt(), self.n, self.ip)


if __name__ == "__main__":
    print("\nTest 1")
    print("======")
    print("p1=x^5+x^2+x")
    print("p2=x^3+x^2+1")
    p1 = Polynomial2([0, 1, 1, 0, 0, 1])
    p2 = Polynomial2([1, 0, 1, 1])
    p3 = p1.add(p2)
    print("p3= p1+p2 = ", p3)

    print("\nTest 2")
    print("======")
    print("p4=x^7+x^4+x^3+x^2+x")
    print("modp=x^8+x^7+x^5+x^4+1")
    p4 = Polynomial2([0, 1, 1, 1, 1, 0, 0, 1])
    # modp=Polynomial2([1,1,0,1,1,0,0,0,1])
    modp = Polynomial2([1, 0, 0, 0, 1, 1, 0, 1, 1])
    p5 = p1.mul(p4, modp)
    print("p5=p1*p4 mod (modp)=", p5)

    print("\nTest 3")
    print("======")
    print("p6=x^12+x^7+x^2")
    print("p7=x^8+x^4+x^3+x+1")
    p6 = Polynomial2([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    p7 = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
    p8q, p8r = p6.div(p7)
    print("q for p6/p7=", p8q)
    print("r for p6/p7=", p8r)

    ####
    print("\nTest 4")
    print("======")
    g1 = GF2N(100)
    g2 = GF2N(5)
    print("g1 = ", g1.getPolynomial2())
    print("g2 = ", g2.getPolynomial2())
    g3 = g1.add(g2)
    print("g1+g2 = ", g3)

    print("\nTest 5")
    print("======")
    ip = Polynomial2([1, 1, 0, 0, 1])
    print("irreducible polynomial", ip)
    g4 = GF2N(0b1101, 4, ip)
    g5 = GF2N(0b110, 4, ip)
    print("g4 = ", g4.getPolynomial2())
    print("g5 = ", g5.getPolynomial2())
    g6 = g4.mul(g5)
    print("g4 x g5 = ", g6.p)

    print("\nTest 6")
    print("======")
    g7 = GF2N(0b1000010000100, 13, None)
    g8 = GF2N(0b100011011, 13, None)
    print("g7 = ", g7.getPolynomial2())
    print("g8 = ", g8.getPolynomial2())
    q, r = g7.div(g8)
    print("g7/g8 =")
    print("q = ", q.getPolynomial2())
    print("r = ", r.getPolynomial2())

    print("\nTest 7")
    print("======")
    ip = Polynomial2([1, 1, 0, 0, 1])
    print("irreducible polynomial", ip)
    g9 = GF2N(0b101, 4, ip)
    print("g9 = ", g9.getPolynomial2())
    print("inverse of g9 =", g9.mulInv().getPolynomial2())

    print("\nTest 8")
    print("======")
    ip = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
    print("irreducible polynomial", ip)
    g10 = GF2N(0xC2, 8, ip)
    print("g10 = 0xc2")
    g11 = g10.mulInv()
    print("inverse of g10 = g11 =", hex(g11.getInt()))
    g12 = g11.affineMap()
    print("affine map of g11 =", hex(g12.getInt()))
