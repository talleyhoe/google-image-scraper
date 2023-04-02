import os, sys, unittest
from random import shuffle

rootdir = os.path.abspath('./')
sys.path.insert(1, rootdir)
from src.cli import get_arguments

# Directory specification is a testing weakpoint
class TestCli(unittest.TestCase):

    def test_nokeyword(self):
        argv = ['cli.py']
        with self.assertRaises(SystemExit):
            get_arguments(argv)

        argv = ['cli.py', '-d', 'test']
        with self.assertRaises(SystemExit):
            get_arguments(argv)

    def test_defaults(self):
        argv = ['cli.py', 'tux']
        args = get_arguments(argv)
        self.assertEqual(args.keyword, ['tux'],
                         "Keyword: {} should be ['tux']".format(args.keyword))
        self.assertEqual(args.count, 10,
                         "Count: {} should be 10".format(args.count))
        self.assertEqual(args.threads, 1, 
                         "Threads: {} should be 1".format(args.threads))

    def test_flags_short(self):
        argv0 = 'cli.py'
        arg_key = ['tux']
        arg_cnt = ['-c', '1000']
        arg_dir = ['-d', 'test']
        arg_thr = ['-t', '999']

        # Shuffle the arguments around randomly
        arg_arr = [arg_key, arg_cnt, arg_dir, arg_thr]
        shuffle(arg_arr)
        argv = [item for subl in arg_arr for item in subl]
        argv.insert(0, argv0)

        args = get_arguments(argv)
        self.assertEqual(args.keyword, ['tux'],
                         "Keyword: {} should be ['tux']".format(args.keyword))
        self.assertEqual(args.count, 1000,
                         "Count: {} should be 1000".format(args.count))
        self.assertEqual(args.threads, 999, 
                         "Threads: {} should be 999".format(args.threads))
        self.assertEqual(args.directory, 'test',
                         "Directory: {} should be 'test'"
                         .format(args.directory))

    def test_flags_long(self):
        argv0 = 'cli.py'
        arg_key = ['tux']
        arg_cnt = ['--count', '1000']
        arg_dir = ['--directory', 'test']
        arg_thr = ['--threads', '999']

        # Shuffle the arguments around randomly
        arg_arr = [arg_key, arg_cnt, arg_dir, arg_thr]
        shuffle(arg_arr)
        argv = [item for subl in arg_arr for item in subl]
        argv.insert(0, argv0)

        args = get_arguments(argv)
        self.assertEqual(args.keyword, ['tux'],
                         "Keyword: {} should be ['tux']".format(args.keyword))
        self.assertEqual(args.count, 1000,
                         "Count: {} should be 1000".format(args.count))
        self.assertEqual(args.threads, 999, 
                         "Threads: {} should be 999".format(args.threads))
        self.assertEqual(args.directory, 'test',
                         "Directory: {} should be 'test'"
                         .format(args.directory))
        
    def test_invalid_values(self):
        argv = ['cli.py', 'tux', '-c' '-2']
        with self.assertRaises(SystemExit):
            get_arguments(argv)

        argv = ['cli.py', 'tux', '-t' '-4300000000']
        with self.assertRaises(SystemExit):
            get_arguments(argv)

        argv = ['cli.py', 'tux', '-c' '-4300000000', '-t', '-49234']
        with self.assertRaises(SystemExit):
            get_arguments(argv)


if __name__ == "__main__":
    unittest.main()

