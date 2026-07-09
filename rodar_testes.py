import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="testes")
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)