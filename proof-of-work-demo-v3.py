#!/usr/bin/env python
# example of proof-of-work algorithm
import hashlib
import time
import pandas as pd

max_nonce = 2 ** 32  # 4 billion


def proof_of_work(header, difficulty_bits):
    # calculate the difficulty target
    target = 2 ** (256 - difficulty_bits)
    for nonce in range(max_nonce):
        hash_result = hashlib.sha256((str(header) + str(nonce)).encode('utf-8')).hexdigest()
        # check if this is a valid result, below the target
        if int(hash_result, 16) < target:
            print("Success with nonce %d" % nonce)
            print("Hash is %s" % hash_result)
            return (hash_result, nonce)
    print("Failed after %d (max_nonce) tries" % nonce)
    return nonce


if __name__ == '__main__':
    nonce = 0
    hash_result = ''
    # difficulty from 0 to 31 bits
    data_all = []
    for difficulty_bits in range(32):
        data_row = []

        difficulty = 2 ** difficulty_bits
        print("Difficulty: %ld (%d bits)" % (difficulty, difficulty_bits))
        data_row.append(difficulty)
        data_row.append(difficulty_bits)

        print("Starting search...")
        # checkpoint the current time
        start_time = time.time()
        # make a new block which includes the hash from the previous block
        # we fake a block of transactions - just a string
        new_block = 'test block with transactions' + hash_result
        # find a valid nonce for the new block
        (hash_result, nonce) = proof_of_work(new_block, difficulty_bits)
        # checkpoint how long it took to find a result
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed Time: %.5f seconds" % elapsed_time)
        data_row.append(elapsed_time)

        if elapsed_time > 0:
            # estimate the hashes per second
            hash_power = float(int(nonce) / elapsed_time)
            print("Hashing Power: %ld hashes per second" % hash_power)
            data_row.append(hash_power)
        else:
            data_row.append('')

        data_row.append(nonce)
        data_all.append(data_row)

    # pd.set_option('display.float_format',lambda x : '%.2f' % x)
    df = pd.DataFrame(data=data_all, columns=['difficulty', 'bits', 'time(seconds)', 'power(hashes/second)', 'nonce'])
    # df.round({})
    df['power(hashes/second)'] = df['power(hashes/second)'].map(lambda x: '%d' % x)
    df.to_csv('result.csv',float_format='%.5f')
