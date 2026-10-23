"""Small deterministic checks, not financial model validation."""
import contextlib
import importlib.util
import io
from pathlib import Path
import random
import unittest
from unittest.mock import patch


class SimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = []
        for filename in ("mc_fire.py", "mc_fire_10yr.py", "mc_fire_grid.py"):
            spec = importlib.util.spec_from_file_location(filename[:-3], Path(__file__).with_name(filename))
            module = importlib.util.module_from_spec(spec)
            before = random.getstate()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                spec.loader.exec_module(module)
            if output.getvalue() or random.getstate() != before:
                raise AssertionError("Import must not print, simulate or reseed global randomness")
            module.N = 8
            module.INFL = 0.0
            if hasattr(module, "TAX_DRAG"):
                module.TAX_DRAG = 0.0
            cls.modules.append(module)

    @staticmethod
    def run_case(module, start, onetime, expense, sampled_return=0.0):
        if hasattr(module, "run10"):
            module.START, module.ONE, module.UNI, module.RET = start, onetime, expense, expense
            draws = 0
            def final_period_return(mean, sd):
                nonlocal draws
                draws += 1
                return sampled_return if draws % 10 == 0 else 0.0
            return module.run10(0.0, 0.0, final_period_return)
        with patch.object(module.random, "gauss", return_value=sampled_return):
            return module.run(start, onetime, expense, expense, 0, 1, 0.0, 0.0)

    def test_zero_return_preserves_unspent_units(self):
        for module in self.modules:
            with self.subTest(module=module.__name__):
                result = self.run_case(module, 1.0, 0.1, 0.0)
                self.assertEqual(result[0], 100.0)
                self.assertAlmostEqual(result[-1], 0.9)

    def test_upfront_ruin_fails(self):
        for module in self.modules:
            with self.subTest(module=module.__name__):
                self.assertEqual(self.run_case(module, 0.1, 0.2, 0.0)[0], 0.0)

    def test_terminal_nonpositive_balance_is_ruin(self):
        for module in self.modules:
            for sampled_return in (-1.0, -2.0):
                with self.subTest(module=module.__name__, sampled_return=sampled_return):
                    result = self.run_case(module, 1.0, 0.0, 0.0, sampled_return)
                    self.assertEqual(result[0], 0.0)
                    self.assertEqual(result[-1], 0.0)

    def test_scale_invariance(self):
        for module in self.modules:
            with self.subTest(module=module.__name__):
                small = self.run_case(module, 1.0, 0.1, 0.01)
                large = self.run_case(module, 10.0, 1.0, 0.1)
                self.assertEqual(small[0], large[0])
                self.assertAlmostEqual(small[-1] * 10.0, large[-1])


if __name__ == "__main__":
    unittest.main()
