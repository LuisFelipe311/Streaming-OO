"""Executa toda a suíte de testes do projeto (pasta testes/).

Uso (na raiz do projeto):
    python rodar_testes.py

Equivale a rodar: python -m unittest discover -s testes -v
"""

import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="testes")
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
