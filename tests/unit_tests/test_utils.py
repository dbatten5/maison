"""Tests for the `utils` module."""

import pytest

from maison.utils import deep_merge


class TestDeepMerge:
    """Tests for the `deep_merge` function."""

    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            pytest.param(
                {1: 2, 3: 4},
                {3: 5, 6: 7},
                {1: 2, 3: 5, 6: 7},
                id="simple",
            ),
            pytest.param(
                {1: 2, 3: {4: 5, 6: 7}},
                {3: {6: 8, 9: 10}, 11: 12},
                {1: 2, 3: {4: 5, 6: 8, 9: 10}, 11: 12},
                id="nested",
            ),
        ],
    )
    def test_success(
        self,
        a: dict[int, int],
        b: dict[int, int],
        expected: dict[int, int],
    ) -> None:
        assert deep_merge(a, b) == expected
        assert a == expected

    def test_incompatible_dicts(self) -> None:
        """Trying to merge incompatible dicts returns an error"""
        dict_a = {1: 2, 2: 5}
        dict_b = {1: {3: 4}}

        with pytest.raises(RuntimeError):
            deep_merge(dict_a, dict_b)
