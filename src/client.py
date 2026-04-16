from encoder.encoder import split_secret

def main():
    secret, threshold, total_shares = input().split()

    threshold = int(threshold)
    total_shares = int(total_shares)
    shares = split_secret(secret, threshold, total_shares)

    print(shares)


if __name__ == "__main__":
    main()
