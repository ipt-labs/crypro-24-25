import unittest
from subprograms import gcdEuclideanExtended2, linearCongruence

class TestGcdEuclideanExtended2(unittest.TestCase):
    # Find reverse element in Zm
    def test_gcdEuclideanExtended2_reverse_01(self):
        self.assertEqual(gcdEuclideanExtended2(0, 0), (0, 0))

    def test_gcdEuclideanExtended2_reverse_02(self):
        self.assertEqual(gcdEuclideanExtended2(0, 1), (1, 0))

    def test_gcdEuclideanExtended2_reverse_03(self):
        self.assertEqual(gcdEuclideanExtended2(1, 0), (1, 0))

    def test_gcdEuclideanExtended2_reverse_04(self):
        self.assertEqual(gcdEuclideanExtended2(1, 1), (1, 0))

    def test_gcdEuclideanExtended2_reverse_05(self):
        self.assertEqual(gcdEuclideanExtended2(2, 3), (1, 2))

    def test_gcdEuclideanExtended2_reverse_06(self):
        self.assertEqual(gcdEuclideanExtended2(2, 5), (1, 3))

    def test_gcdEuclideanExtended2_reverse_07(self):
        self.assertEqual(gcdEuclideanExtended2(5, 11), (1, 9))

    def test_gcdEuclideanExtended2_reverse_08(self):
        self.assertEqual(gcdEuclideanExtended2(3, 20), (1, 7))

    def test_gcdEuclideanExtended2_reverse_09(self):
        self.assertEqual(gcdEuclideanExtended2(9, 13), (1, 3))

    # Find gcd
    def test_gcdEuclideanExtended2_gcd_01(self):
        gcd, _ = gcdEuclideanExtended2(0, 0)
        self.assertEqual(0, gcd)

    def test_gcdEuclideanExtended2_gcd_02(self):
        gcd, _ = gcdEuclideanExtended2(0, 1)
        self.assertEqual(1, gcd)

    def test_gcdEuclideanExtended2_gcd_03(self):
        gcd, _ = gcdEuclideanExtended2(1, 0)
        self.assertEqual(1, gcd)

    def test_gcdEuclideanExtended2_gcd_04(self):
        gcd, _ = gcdEuclideanExtended2(1, 1)
        self.assertEqual(1, gcd)

    def test_gcdEuclideanExtended2_gcd_05(self):
        gcd, _ = gcdEuclideanExtended2(2, 3)
        self.assertEqual(1, gcd)

    def test_gcdEuclideanExtended2_gcd_06(self):
        gcd, _ = gcdEuclideanExtended2(2, 5)
        self.assertEqual(1, gcd)

    def test_gcdEuclideanExtended2_gcd_07(self):
        gcd, _ = gcdEuclideanExtended2(5, 11)
        self.assertEqual(1, gcd)

    def test_gcdEuclideanExtended2_gcd_08(self):
        gcd, _ = gcdEuclideanExtended2(3, 20)
        self.assertEqual(1, gcd)

    def test_gcdEuclideanExtended2_gcd_09(self):
        gcd, _ = gcdEuclideanExtended2(9, 13)
        self.assertEqual(1, gcd)

    def test_gcdEuclideanExtended2_gcd_10(self):
        gcd, _ = gcdEuclideanExtended2(6, 9)
        self.assertEqual(3, gcd)

    def test_gcdEuclideanExtended2_gcd_11(self):
        gcd, _ = gcdEuclideanExtended2(12, 15)
        self.assertEqual(3, gcd)

    def test_gcdEuclideanExtended2_gcd_12(self):
        gcd, _ = gcdEuclideanExtended2(14, 21)
        self.assertEqual(7, gcd)

    def test_gcdEuclideanExtended2_gcd_13(self):
        gcd, _ = gcdEuclideanExtended2(18, 24)
        self.assertEqual(6, gcd)

    def test_gcdEuclideanExtended2_gcd_14(self):
        gcd, _ = gcdEuclideanExtended2(35, 49)
        self.assertEqual(7, gcd)

    def test_gcdEuclideanExtended2_gcd_15(self):
        gcd, _ = gcdEuclideanExtended2(27, 36)
        self.assertEqual(9, gcd)

    def test_gcdEuclideanExtended2_gcd_16(self):
        gcd, _ = gcdEuclideanExtended2(20, 30)
        self.assertEqual(10, gcd)

    def test_gcdEuclideanExtended2_gcd_17(self):
        gcd, _ = gcdEuclideanExtended2(25, 35)
        self.assertEqual(5, gcd)

    def test_gcdEuclideanExtended2_gcd_18(self):
        gcd, _ = gcdEuclideanExtended2(40, 60)
        self.assertEqual(20, gcd)

    def test_gcdEuclideanExtended2_gcd_19(self):
        gcd, _ = gcdEuclideanExtended2(50, 75)
        self.assertEqual(25, gcd)

class TestLinearCongruence(unittest.TestCase):
    def test_linearCongruence_01(self):
        self.assertEqual(linearCongruence(1, 1, 1), ([0], False))

    def test_linearCongruence_02(self):
        self.assertEqual(linearCongruence(2, 3, 5), ([4], False))

    def test_linearCongruence_03(self):
        self.assertEqual(linearCongruence(4, 6, 8), ([], True))

    def test_linearCongruence_04(self):
        self.assertEqual(linearCongruence(3, 6, 9), ([2, 5, 8], False))

    def test_linearCongruence_05(self):
        self.assertEqual(linearCongruence(7, 5, 13), ([10], False))

    def test_linearCongruence_06(self):
        self.assertEqual(linearCongruence(10, 15, 25), ([4, 9, 14, 19, 24], False))

    def test_linearCongruence_07(self):
        self.assertEqual(linearCongruence(12, 18, 24), ([], True))

    def test_linearCongruence_08(self):
        self.assertEqual(linearCongruence(5, 10, 15), ([2, 5, 8, 11, 14], False))

    def test_linearCongruence_09(self):
        self.assertEqual(linearCongruence(8, 16, 20), ([2, 7, 12, 17], False))

    def test_linearCongruence_10(self):
        self.assertEqual(linearCongruence(9, 27, 30), ([3, 13, 23], False))


if __name__ == "__main__":
  unittest.main()
