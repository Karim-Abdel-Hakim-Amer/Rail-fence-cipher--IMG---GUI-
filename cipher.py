def rail_fence_encrypt(data, rails):
    # Create empty lists for each rail
    fence = [[] for _ in range(rails)]
    rail = 0           # Current rail index
    direction = 1      # Direction: 1 = down, -1 = up

    # Place each item in the appropriate rail in a zig-zag pattern
    for item in data:
        fence[rail].append(item)
        rail += direction

        # Change direction when reaching top or bottom rail
        if rail == 0 or rail == rails - 1:
            direction *= -1

    # Flatten rails row by row to get encrypted sequence
    return [item for r in fence for item in r]


def rail_fence_decrypt(data, rails):
    n = len(data)

    # Build the zig-zag pattern (which rail each index belongs to)
    pattern = []
    rail = 0
    direction = 1
    for _ in range(n):
        pattern.append(rail)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    # Count how many elements go into each rail
    rail_counts = [pattern.count(r) for r in range(rails)]

    # Slice the encrypted data into separate rails
    rails_data = []
    idx = 0
    for count in rail_counts:
        rails_data.append(data[idx:idx + count])
        idx += count

    # Reconstruct original order using the zig-zag pattern
    rail_indices = [0] * rails  # Track current index for each rail
    decrypted = []

    for r in pattern:
        decrypted.append(rails_data[r][rail_indices[r]])
        rail_indices[r] += 1

    return decrypted
