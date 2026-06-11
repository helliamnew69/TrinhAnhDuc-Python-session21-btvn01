import unittest

from main import (
    Wallet,
    InvalidAmountError,
    InsufficientBalanceError
)


class TestWallet(unittest.TestCase):
    """Unit tests for Wallet class."""

    def test_deposit_success(self):
        """
        Deposit should increase balance.
        """

        wallet = Wallet()

        wallet.deposit(500000)

        self.assertEqual(
            wallet.balance,
            500000
        )

    def test_transfer_insufficient_balance(self):
        """
        Transfer should raise
        InsufficientBalanceError.
        """

        wallet = Wallet()

        wallet.deposit(100000)

        with self.assertRaises(
            InsufficientBalanceError
        ):
            wallet.transfer(
                "0987654321",
                500000
            )

    def test_invalid_amount(self):
        """
        Deposit negative amount
        should raise InvalidAmountError.
        """

        wallet = Wallet()

        with self.assertRaises(
            InvalidAmountError
        ):
            wallet.deposit(-1000)


if __name__ == "__main__":
    unittest.main()