import logging
import os


logging.basicConfig(
    filename="momo_transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class InvalidAmountError(Exception):
    """Raised when transaction amount is invalid."""


class InsufficientBalanceError(Exception):
    """Raised when wallet balance is insufficient."""


class Wallet:
    """Represent a MoMo wallet."""

    def __init__(self):
        """Initialize wallet with zero balance."""
        self.balance = 0

    def deposit(self, amount):
        """
        Deposit money into wallet.

        Args:
            amount (int): Amount to deposit.

        Raises:
            InvalidAmountError
        """
        if amount <= 0:
            raise InvalidAmountError

        self.balance += amount

    def transfer(self, phone_number, amount):
        """
        Transfer money to another user.

        Args:
            phone_number (str): Receiver phone number.
            amount (int): Transfer amount.

        Raises:
            InvalidAmountError
            InsufficientBalanceError
        """
        if amount <= 0:
            raise InvalidAmountError

        if amount > self.balance:
            raise InsufficientBalanceError

        self.balance -= amount

        return phone_number


def display_menu():
    """Display main menu."""

    print("\n========== VÍ MOMO GIẢ LẬP ==========")
    print("1. Nạp tiền vào ví")
    print("2. Chuyển tiền")
    print("3. Xem lịch sử hệ thống")
    print("4. Xem số dư tài khoản")
    print("5. Thoát chương trình")
    print("=====================================")


def input_positive_amount():
    """
    Get valid amount from user.

    Returns:
        int
    """

    while True:
        try:
            amount = int(input("Nhập số tiền: "))
            return amount

        except ValueError:
            logging.error(
                "ValueError: Invalid numeric input."
            )
            print("Lỗi: Vui lòng nhập số tiền hợp lệ.")


def deposit_money(wallet):
    """
    Handle deposit feature.

    Args:
        wallet (Wallet)
    """

    print("\n--- NẠP TIỀN VÀO VÍ ---")

    while True:
        amount = input_positive_amount()

        try:
            wallet.deposit(amount)

            logging.info(
                f"Deposit successful: +{amount} VND. "
                f"Current Balance: {wallet.balance}"
            )

            print(
                f"\nNạp tiền thành công: +{amount:,} VND"
            )
            print(
                f"Số dư hiện tại: {wallet.balance:,} VND"
            )

            break

        except InvalidAmountError:
            logging.error(
                f"InvalidAmountError: "
                f"Attempted to process {amount} VND."
            )
            print(
                "Lỗi: Số tiền giao dịch phải lớn hơn 0."
            )


def get_valid_phone():
    """
    Get valid phone number.

    Returns:
        str
    """

    while True:
        phone = input(
            "Nhập số điện thoại người nhận: "
        ).strip()

        if phone.isdigit() and len(phone) == 10:
            return phone

        print(
            "Số điện thoại phải gồm đúng 10 chữ số."
        )


def transfer_money(wallet):
    """
    Handle transfer feature.

    Args:
        wallet (Wallet)
    """

    print("\n--- CHUYỂN TIỀN ---")

    phone_number = get_valid_phone()

    while True:
        try:
            amount = int(
                input("Nhập số tiền cần chuyển: ")
            )

            if amount >= 10_000_000:
                logging.warning(
                    "High value transaction detected: "
                    f"{amount} VND to {phone_number}"
                )

            wallet.transfer(phone_number, amount)

            logging.info(
                f"Transfer successful: -{amount} VND "
                f"to {phone_number}. "
                f"Current Balance: {wallet.balance}"
            )

            print(
                f"\nChuyển tiền thành công tới "
                f"số điện thoại {phone_number}."
            )
            print(
                f"Số tiền đã chuyển: {amount:,} VND"
            )
            print(
                f"Số dư còn lại: "
                f"{wallet.balance:,} VND"
            )

            break

        except ValueError:
            logging.error(
                "ValueError: Invalid numeric input "
                "for transfer."
            )
            print(
                "Lỗi: Vui lòng nhập số tiền hợp lệ."
            )

        except InvalidAmountError:
            logging.error(
                f"InvalidAmountError: "
                f"Attempted to process {amount} VND."
            )
            print(
                "Lỗi: Số tiền giao dịch phải lớn hơn 0."
            )

        except InsufficientBalanceError:
            logging.error(
                "InsufficientBalanceError: "
                f"Attempted to transfer {amount} VND "
                f"with balance {wallet.balance} VND."
            )

            print(
                "\nGiao dịch thất bại: "
                "Số dư của bạn không đủ."
            )
            print(
                f"Số dư hiện tại: "
                f"{wallet.balance:,} VND"
            )
            break


def read_logs():
    """Display latest 5 log records."""

    print(
        "\n--- 5 SỰ KIỆN GẦN NHẤT "
        "TRONG HỆ THỐNG ---"
    )

    if not os.path.exists(
        "momo_transactions.log"
    ):
        print(
            "Chưa có lịch sử giao dịch nào "
            "trong hệ thống."
        )
        return

    with open(
        "momo_transactions.log",
        "r",
        encoding="utf-8"
    ) as file:
        lines = file.readlines()

    if not lines:
        print(
            "Chưa có lịch sử giao dịch nào "
            "trong hệ thống."
        )
        return

    for index, line in enumerate(
        lines[-5:], start=1
    ):
        print(f"{index}. {line.strip()}")


def show_balance(wallet):
    """
    Display wallet balance.

    Args:
        wallet (Wallet)
    """

    logging.info(
        f"Balance checked. "
        f"Current Balance: {wallet.balance}"
    )

    print("\n--- SỐ DƯ VÍ MOMO ---")
    print(
        f"Số dư hiện tại: "
        f"{wallet.balance:,} VND"
    )


def main():
    """Program entry point."""

    wallet = Wallet()

    while True:
        display_menu()

        choice = input(
            "Chọn chức năng (1-5): "
        )

        if choice == "1":
            deposit_money(wallet)

        elif choice == "2":
            transfer_money(wallet)

        elif choice == "3":
            read_logs()

        elif choice == "4":
            show_balance(wallet)

        elif choice == "5":
            logging.info(
                "Wallet application closed."
            )

            print(
                "\nCảm ơn bạn đã sử dụng "
                "dịch vụ."
            )
            break

        else:
            print(
                "Lựa chọn không hợp lệ."
            )


if __name__ == "__main__":
    main()