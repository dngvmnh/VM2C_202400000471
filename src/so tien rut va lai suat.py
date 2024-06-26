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
    'Tháng': pd.date_range(start='2025-01-01', periods=months, freq='M'),
    'Số tiền rút (tỉ đồng)': withdrawals,
    'Thời gian đáo hạn (tháng)': durations
})

# Tính lãi suất hàng tháng từ lãi suất 3.5% theo năm
fixed_annual_interest_rate = 0.035
fixed_monthly_interest_rate = (1 + fixed_annual_interest_rate)**(1/12) - 1

# Tính toán lãi suất dao động hàng tháng và hàng năm
fluctuation_factor = 0.5
monthly_update = []

for month in range(months):
    # Điều chỉnh lãi suất hàng năm với dao động nhỏ
    fluctuation = np.random.uniform(-fluctuation_factor, fluctuation_factor)
    current_annual_interest_rate = annual_interest_rate * (1 + fluctuation)
    current_monthly_interest_rate = (1 + current_annual_interest_rate)**(1/12) - 1
    
    # Lưu trữ thông tin cập nhật mỗi tháng
    monthly_update.append({
        'Tháng': df['Tháng'][month],
        'Số tiền rút (tỉ đồng)': withdrawals[month],
        'Lãi suất hàng tháng': current_monthly_interest_rate,
        'Lãi suất hàng năm': current_annual_interest_rate
    })

# Tạo DataFrame từ thông tin cập nhật mỗi tháng
df_update = pd.DataFrame(monthly_update)

# Xuất bảng cập nhật các tháng
print("\nBảng cập nhật các tháng:")
print(df_update)

# Vẽ biểu đồ thể hiện mối tương quan giữa lãi suất hàng tháng và số tiền rút
fig, ax1 = plt.subplots(figsize=(14, 7))

ax1.set_xlabel('Tháng')
ax1.set_ylabel('Số tiền rút (tỉ đồng)', color='tab:blue')
ax1.plot(df_update['Tháng'], df_update['Số tiền rút (tỉ đồng)'], marker='o', color='tab:blue', label='Số tiền rút')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Lãi suất hàng tháng', color='tab:red')
ax2.plot(df_update['Tháng'], df_update['Lãi suất hàng tháng'], marker='x', color='tab:red', label='Lãi suất hàng tháng')
ax2.axhline(y=fixed_monthly_interest_rate, color='green', linestyle='--', linewidth=2, label='Lãi suất cố định hàng tháng (3.5% năm)')
ax2.tick_params(axis='y', labelcolor='tab:red')

fig.tight_layout()
plt.title('Mối tương quan giữa Lãi suất và Số tiền rút từ 2025 đến 2034')
fig.legend(loc='upper left')
plt.grid(True)
plt.show()
