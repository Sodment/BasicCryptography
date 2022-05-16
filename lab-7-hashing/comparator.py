import readline
import sys

file_to_compare = "lab-7-hashing/zad4.txt"

if __name__ == "__main__":
    with open(file_to_compare) as f:
        content = f.readlines()
        hash_one = content[0].strip().replace(" ", "")
        hash_two = content[1].strip().replace(" ", "")

        hash_one = ''.join(format(ord(x), 'b') for x in hash_one)
        hash_two = ''.join(format(ord(x), 'b') for x in hash_two)

        print(f"Original message: {hash_one}")
        print(f"Modified message: {hash_two}")

        diff = []
        counter = 0

        for i in range(min([len(hash_two), len(hash_one)])):
            if hash_one[i] != hash_two[i]:
                counter += 1
                diff.append((i, hash_one[i], hash_two[i]))

        print(
            f'Diffrence betweeen two hashes is {counter} and length of hash is {len(hash_one)}')
        print("Original message --> Modified Message")

        for x in diff:
            print(f"{x[1]} --> {x[2]} at position {x[0]}")
