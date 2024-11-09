import threading
from random import randint
from time import sleep
from tkinter.ttk import Treeview


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        if self.balance< 500 and not self.lock.locked():
            for _ in range(100):
                num = randint(50, 500)
                self.balance += num
                print(f'Пополнение: {num}. Баланс: {self.balance}')
                sleep(0.001)
        elif self.balance >= 500 and self.lock.locked():
            self.lock.release()

    def take(self):
        for n in range(100):
            num = randint(50, 500)
            if num <= self.balance and not self.lock.locked():
                    print(f'Запрос на {num}')
                    self.balance -= num
                    print(f'Снятие: {num}. Баланс: {self.balance}')
                    sleep(0.001)
            elif num > self.balance:
                print(f'Запрос отклонён, недостаточно средств')
                self.lock.acquire()
                sleep(0.001)
            else:
                self.lock.release()


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
