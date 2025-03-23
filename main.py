import random
import pandas as pd
from itertools import combinations
from tkinter import *
from tkinter import messagebox

# ایجاد دیتاست تصادفی از تراکنش‌ها
def create_random_dataset(num_transactions, num_items):
    dataset = []
    for _ in range(num_transactions):
        transaction = random.sample(range(1, num_items + 1), random.randint(1, num_items))
        dataset.append(transaction)
    return dataset

# تبدیل دیتاست به فرمت مناسب برای الگوریتم‌ها
def encode_transactions(dataset):
    unique_items = set(item for transaction in dataset for item in transaction)
    encoded_dataset = []
    for transaction in dataset:
        encoded_transaction = {item: (item in transaction) for item in unique_items}
        encoded_dataset.append(encoded_transaction)
    return pd.DataFrame(encoded_dataset)

# الگوریتم Apriori
def run_apriori(dataset, min_support):
    unique_items = set(item for transaction in dataset for item in transaction)
    frequent_itemsets = []

    # مرحله ۱: ایجاد مجموعه‌های تک‌عضوی
    candidates = [frozenset([item]) for item in unique_items]
    k = 1

    while candidates:
        # شمارش فراوانی هر کاندید
        candidate_counts = {}
        for transaction in dataset:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    candidate_counts[candidate] = candidate_counts.get(candidate, 0) + 1

        # فیلتر کردن بر اساس حداقل پشتیبانی
        frequent_k_itemsets = [
            (itemset, support / len(dataset))
            for itemset, support in candidate_counts.items()
            if support / len(dataset) >= min_support
        ]
        frequent_itemsets.extend(frequent_k_itemsets)

        # ایجاد کاندیدهای جدید برای مرحله بعدی
        candidates = generate_candidates(frequent_k_itemsets, k)
        k += 1

    return frequent_itemsets

# ایجاد کاندیدهای جدید برای Apriori
def generate_candidates(frequent_itemsets, k):
    candidates = set()
    for i in range(len(frequent_itemsets)):
        for j in range(i + 1, len(frequent_itemsets)):
            itemset1 = frequent_itemsets[i][0]
            itemset2 = frequent_itemsets[j][0]
            if len(itemset1.union(itemset2)) == k + 1:
                candidates.add(itemset1.union(itemset2))
    return list(candidates)

# الگوریتم AprioriTID
def run_apriori_tid(dataset, min_support):
    unique_items = set(item for transaction in dataset for item in transaction)
    frequent_itemsets = []

    # مرحله ۱: ایجاد مجموعه‌های تک‌عضوی
    candidates = [frozenset([item]) for item in unique_items]
    k = 1

    while candidates:
        # شمارش فراوانی هر کاندید
        candidate_counts = {}
        for transaction in dataset:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    candidate_counts[candidate] = candidate_counts.get(candidate, 0) + 1

        # فیلتر کردن بر اساس حداقل پشتیبانی
        frequent_k_itemsets = [
            (itemset, support / len(dataset))
            for itemset, support in candidate_counts.items()
            if support / len(dataset) >= min_support
        ]
        frequent_itemsets.extend(frequent_k_itemsets)

        # ایجاد کاندیدهای جدید برای مرحله بعدی
        candidates = generate_candidates(frequent_k_itemsets, k)
        k += 1

    return frequent_itemsets

# الگوریتم AIS
def run_ais(dataset, min_support):
    unique_items = set(item for transaction in dataset for item in transaction)
    frequent_itemsets = []

    # شمارش فراوانی آیتم‌ها
    item_counts = {item: 0 for item in unique_items}
    for transaction in dataset:
        for item in transaction:
            item_counts[item] += 1

    # فیلتر کردن بر اساس حداقل پشتیبانی
    frequent_items = [
        item for item, count in item_counts.items()
        if count / len(dataset) >= min_support
    ]

    # ایجاد مجموعه‌های تک‌عضوی
    frequent_itemsets.extend([(frozenset([item]), item_counts[item] / len(dataset)) for item in frequent_items])

    return frequent_itemsets

# رابط کاربری
def create_gui():
    def on_run_algorithm():
        try:
            num_transactions = int(num_transactions_entry.get())
            num_items = int(num_items_entry.get())
            min_support = float(min_support_entry.get())
        except ValueError:
            messagebox.showerror("خطا", "لطفاً مقادیر معتبر وارد کنید.")
            return

        # ایجاد دیتاست
        global dataset
        dataset = create_random_dataset(num_transactions, num_items)

        selected_algorithm = algorithm_var.get()
        if selected_algorithm == "Apriori":
            result = run_apriori(dataset, min_support)
        elif selected_algorithm == "AprioriTID":
            result = run_apriori_tid(dataset, min_support)
        elif selected_algorithm == "AIS":
            result = run_ais(dataset, min_support)
        else:
            messagebox.showerror("خطا", "الگوریتم انتخاب شده نامعتبر است.")
            return

        # نمایش نتایج
        result_text.delete(1.0, END)
        result_text.insert(END, "نتایج:\n")
        for itemset, support in result:
            result_text.insert(END, f"{set(itemset)}: {support:.2f}\n")

        # پرسش برای ادامه
        if messagebox.askyesno("ادامه", "آیا می‌خواهید الگوریتم دیگری اجرا کنید؟"):
            algorithm_var.set("Apriori")
            min_support_entry.delete(0, END)
        else:
            root.quit()

    root = Tk()
    root.title("پروژه داده‌کاوی")

    Label(root, text="تعداد تراکنش‌ها:").grid(row=0, column=0)
    num_transactions_entry = Entry(root)
    num_transactions_entry.grid(row=0, column=1)

    Label(root, text="تعداد آیتم‌ها:").grid(row=1, column=0)
    num_items_entry = Entry(root)
    num_items_entry.grid(row=1, column=1)

    Label(root, text="انتخاب الگوریتم:").grid(row=2, column=0)
    algorithm_var = StringVar(value="Apriori")
    algorithms = ["Apriori", "AprioriTID", "AIS"]
    algorithm_menu = OptionMenu(root, algorithm_var, *algorithms)
    algorithm_menu.grid(row=2, column=1)

    Label(root, text="حداقل پشتیبانی (min_support):").grid(row=3, column=0)
    min_support_entry = Entry(root)
    min_support_entry.grid(row=3, column=1)

    Button(root, text="اجرای الگوریتم", command=on_run_algorithm).grid(row=4, column=0, columnspan=2)

    result_text = Text(root, height=10, width=50)
    result_text.grid(row=5, column=0, columnspan=2)

    root.mainloop()

# اجرای رابط کاربری
create_gui()