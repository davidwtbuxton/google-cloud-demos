import sys


if __name__ == '__main__':
    import dsexport.cli

    try:
        dsexport.cli.main(sys.argv, sys.stdout)
    except UnicodeDecodeError as err:
        sys.stdout.flush()
        sys.stderr.write('\nError: {}\n'.format(err))
        sys.stderr.write('You can try --bytes=base64 to encode binary values\n')
