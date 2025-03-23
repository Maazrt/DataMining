import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox

# تابع برای خواندن دیتاست از فایل
def read_dataset_from_file(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.txt'):
            df = pd.read_csv(file_path, delimiter='\t')
        else:
            messagebox.showerror("خطا", "فرمت فایل پشتیبانی نمی‌شود.")
            return None
        return df
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در خواندن فایل: {e}")
        return None

# تابع برای تبدیل دیتاست به فرمت مناسب
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

# رابط کاربری
def create_gui():
    def on_run_algorithm():
        try:
            min_support = float(min_support_entry.get())
        except ValueError:
            messagebox.showerror("خطا", "لطفاً حداقل پشتیبانی را به صورت عدد وارد کنید.")
            return

        # خواندن دیتاست
        if dataset_source.get() == "file":
            file_path = file_path_entry.get()
            if not file_path:
                messagebox.showerror("خطا", "لطفاً آدرس فایل را وارد کنید.")
                return
            df = read_dataset_from_file(file_path)
            if df is None:
                return
            dataset = df.values.tolist()
        else:
            dataset = manual_dataset_entry.get("1.0", END).strip().split('\n')
            dataset = [list(map(int, transaction.split(','))) for transaction in dataset]

        # اجرای الگوریتم
        result = run_apriori(dataset, min_support)

        # نمایش نتایج
        result_text.delete(1.0, END)
        result_text.insert(END, "نتایج:\n")
        for itemset, support in result:
            result_text.insert(END, f"{set(itemset)}: {support:.2f}\n")

    def on_file_select():
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")])
        file_path_entry.delete(0, END)
        file_path_entry.insert(0, file_path)

    root = Tk()
    root.title("پروژه داده‌کاوی")

    # انتخاب منبع دیتاست
    Label(root, text="منبع دیتاست:").grid(row=0, column=0)
    dataset_source = StringVar(value="manual")
    Radiobutton(root, text="ورود دستی دیتاست", variable=dataset_source, value="manual").grid(row=0, column=1)
    Radiobutton(root, text="خواندن از فایل", variable=dataset_source, value="file").grid(row=0, column=2)

    # ورود دستی دیتاست
    Label(root, text="دیتاست (هر تراکنش در یک خط و آیتم‌ها با کاما جدا شده‌اند):").grid(row=1, column=0, columnspan=3)
    manual_dataset_entry = Text(root, height=10, width=50)
    manual_dataset_entry.grid(row=2, column=0, columnspan=3)

    # انتخاب فایل
    Label(root, text="آدرس فایل:").grid(row=3, column=0)
    file_path_entry = Entry(root, width=40)
    file_path_entry.grid(row=3, column=1)
    Button(root, text="انتخاب فایل", command=on_file_select).grid(row=3, column=2)

    # حداقل پشتیبانی
    Label(root, text="حداقل پشتیبانی (min_support):").grid(row=4, column=0)
    min_support_entry = Entry(root)
    min_support_entry.grid(row=4, column=1)

    # دکمه اجرای الگوریتم
    Button(root, text="اجرای الگوریتم", command=on_run_algorithm).grid(row=5, column=0, columnspan=3)

    # نمایش نتایج
    result_text = Text(root, height=10, width=50)
    result_text.grid(row=6, column=0, columnspan=3)

    root.mainloop()

# اجرای رابط کاربری
create_gui()