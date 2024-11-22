import argparse
import random
import string


def generate_id(length: int) -> str:
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
    chars = random.choices(alphabet, k=length)
    return "".join(chars)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("amount", type=int, help="The amount of ids to generate.")
    parser.add_argument(
        "--length",
        type=int,
        default=63,
        help="The length of an id, not including newline.",
    )

    args = parser.parse_args()
    amount = int(args.amount)
    length = int(args.length)

    file = open(f"data/{amount}.data", "w")

    for _ in range(amount):
        id = generate_id(length)
        file.write(id + "\n")

    file.close()
