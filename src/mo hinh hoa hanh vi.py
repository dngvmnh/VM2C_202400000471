import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

annual_interest_rate = 0.029  # Lãi suất cố định hàng năm
monthly_interest_rate = (1 + annual_interest_rate)**(1/12) - 1  # Lãi suất cố định mỗi tháng
months = 120  # Số tháng từ tháng 1/2025 đến tháng 12/2034

withdrawals = []
durations = []
interests = []
current_annual_interest_rates = []

file_path = 'data.csv'

with open(file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        so_tien_rut = int(row['So tien rut'])
        withdrawals.append(so_tien_rut)

with open(file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        thoi_gian_dao_han = int(row['Thoi gian dao han'])
        durations.append(thoi_gian_dao_han)

with open(file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        lai_thang = float(row['Lai thang'])
        interests.append(lai_thang)

with open(file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        lai_nam = float(row['Lai nam'])
        current_annual_interest_rates.append(lai_nam)


# Tạo DataFrame từ dữ liệu mô phỏng
df = pd.DataFrame({
    'Tháng': pd.date_range(start='2014-01-01', periods=months, freq='M'),
    'Số tiền rút (tỉ đồng)': withdrawals,
    'Thời gian đáo hạn (tháng)': durations
})

# Xuất bảng mô phỏng số tiền rút mỗi lần và thời gian đáo hạn
print("Bảng Mô phỏng số tiền rút mỗi lần và thời gian đáo hạn:")
print(df)

# Tính toán tổng chi phí lãi suất
total_interest = 0
balance = 1000  # Số dư ban đầu là 1000 tỉ đồng

# Lưu trữ lịch sử số dư và thời gian đáo hạn
balance_history = []

# Lưu trữ thông tin cập nhật mỗi tháng
monthly_update = []


for month in range(months):
    # Rút tiền vào đầu tháng
    withdrawal_amount = withdrawals[month]
    balance -= withdrawal_amount
    balance_history.append((withdrawal_amount, durations[month]))

    # Cập nhật và trả nợ theo thời gian đáo hạn
    new_balance_history = []
    for amount, duration in balance_history:
        if duration <= 1:
            balance += amount  # Cộng lại tiền khi đến hạn
        else:
            new_balance_history.append((amount, duration - 1))
    balance_history = new_balance_history

    current_annual_interest_rate = current_annual_interest_rates[month]

    interest = interests[month]
    total_interest += balance * interest

    # Lưu trữ thông tin cập nhật mỗi tháng
    monthly_update.append({
        'Tháng': df['Tháng'][month],
        'Số dư': balance,
        'Lãi suất hàng tháng': interest,
        'Lãi suất hàng năm': current_annual_interest_rate
    })

print(f'\nTổng chi phí lãi suất trong {months} tháng: {total_interest:.2f} tỉ đồng')

# Tạo DataFrame từ thông tin cập nhật mỗi tháng
df_update = pd.DataFrame(monthly_update)

# Xuất bảng cập nhật các tháng
print("\nBảng cập nhật các tháng:")
print(df_update)

# Vẽ biểu đồ số tiền rút mỗi tháng và thời gian đáo hạn
fig, ax1 = plt.subplots(figsize=(14, 7))

ax1.set_xlabel('Tháng')
ax1.set_ylabel('Số tiền rút (tỉ đồng)', color='tab:blue')
ax1.plot(df['Tháng'], df['Số tiền rút (tỉ đồng)'], marker='o', color='tab:blue', label='Số tiền rút')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Thời gian đáo hạn (tháng)', color='tab:red')
ax2.plot(df['Tháng'], df['Thời gian đáo hạn (tháng)'], marker='x', color='tab:red', label='Thời gian đáo hạn')
ax2.tick_params(axis='y', labelcolor='tab:red')

fig.tight_layout()
plt.title('Số tiền rút mỗi tháng và thời gian đáo hạn từ 2025 đến 2034')
plt.grid(True)
plt.show()

# Vẽ biểu đồ số dư mỗi tháng
plt.figure(figsize=(14, 7))
plt.plot(df_update['Tháng'], df_update['Số dư'], marker='o', color='tab:green', label='Số dư')
plt.xlabel('Tháng')
plt.ylabel('Số dư (tỉ đồng)')
plt.title('Số dư mỗi tháng từ 2025 đến 2034')
plt.grid(True)
plt.legend()
plt.show()

