import argparse


def make_parser():
    ap = argparse.ArgumentParser(fromfile_prefix_chars='@')
    ap.add_argument('-b', '--host', default='localhost', metavar='HOSTNAME',
                    help="Bind to host (default: `%(default)s`)")
    ap.add_argument('-p', '--port', default=8080, type=int, metavar='PORT',
                    help="Bind to port (default: `%(default)s`)")
    ap.add_argument('-t', '--timeout', default=10, type=int, metavar='TIMEOUT',
                    help="Timeout in seconds (default: `%(default)s`)")
    ap.add_argument('--db-host', default='localhost', type=str,
                    metavar='DB_HOST',
                    help="Database host name (default: `%(default)s`)")
    ap.add_argument('--db-name', default='postgres', type=str,  # TODO: change
                    metavar='DB_NAME',
                    help="Database name (default: `%(default)s`)")
    ap.add_argument('--db-port', default=5432, type=int,
                    metavar='DB_PORT',
                    help="Database port (default: `%(default)s`)")
    ap.add_argument('--db-user', default='postgres', type=str,
                    metavar='DB_USER',
                    help="Database user name (default: `%(default)s`)")
    ap.add_argument('--db-password', default='postgres', type=str,
                    metavar='DB_PASSWORD',
                    help="Database user password (default: `%(default)s`)")
    return ap
