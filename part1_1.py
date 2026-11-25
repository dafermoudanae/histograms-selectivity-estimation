# DAFERMOU CHRISTINA DANAE - 5206
# VALERAS CHRISTOS - 5182

#import matplotlib.pyplot as plt
#import os

ages = []

try:
    with open('final_general.dat', 'r') as file:
        for line in file:
            row_entries = line.split()
            if row_entries:
                age_value = int(row_entries[1])
                ages.append(age_value)
except FileNotFoundError:
    print("Error: 'final_general.dat' not found.")
    exit()

total_elements = len(ages)
num_bins = 10
min_age = min(ages)
max_age = max(ages)



#print("Total ages:",total_elements)

# ------------------------------------------------------#
#               EQUI-WIDTH HISTOGRAM                    #
# ------------------------------------------------------#

bin_width = (max_age - min_age) / num_bins
bin_counts = [0] * num_bins


for age in ages:
        idx = int((age - min_age) / bin_width)
        if idx == num_bins:
            idx = num_bins - 1
        bin_counts[idx] += 1
#print(f"Bin counts for the Equi-width histogram: {bin_counts}")



# ------------------------------------------------------#
#               EQUI-DEPTH HISTOGRAM                    #
# ------------------------------------------------------#

sorted_ages = sorted(ages)
bin_size = total_elements // num_bins
remainder = total_elements % num_bins

#print(sorted_ages)

current_index = 0
equi_depth_bins = []
display_boundaries = []


for i in range(num_bins):
        if i < remainder:
            this_bin_count = bin_size + 1
        else:
            this_bin_count = bin_size

        first_index = current_index
        last_index = current_index + this_bin_count - 1
        age_start = sorted_ages[first_index]
        age_end = sorted_ages[last_index]

        equi_depth_bins.append((age_start, age_end, this_bin_count))
        current_index += this_bin_count
for i, b in enumerate(equi_depth_bins):
    start, end = b[0], b[1]

    if i == len(equi_depth_bins) - 1:
        display_boundaries.append(f"[{start}-{end}]")
    else:
        display_boundaries.append(f"[{start}-{end})")

#print(f"Equi-depth histogram boundaries: [ {', '.join(display_boundaries)} ]")

#------------------------------------------------------#
#                 MATLAB EXPORT                        #
#------------------------------------------------------#

# folder_name = "histograms 1.1"
# os.makedirs(folder_name, exist_ok=True)

#Equal-width Histogram:

width_labels = []
for i in range(num_bins):
    start = int(min_age + i * bin_width)
    end = int(min_age + (i + 1) * bin_width)

    if i == 0:
        width_labels.append(f"<={end}")
    elif i == num_bins - 1:
        width_labels.append(f">{start}")
    else:
        width_labels.append(f"{start}-{end}")

# plt.figure(figsize=(12, 6))
# plt.bar(range(num_bins), bin_counts, color='skyblue', edgecolor='black', alpha=0.8)
# plt.title('Equi-width Histogram')
# plt.xlabel('Ages')
# plt.ylabel('Frequency')
# plt.xticks(range(num_bins), width_labels, rotation=0)
# plt.grid(axis='y', linestyle='--', alpha=0.5)
# plt.tight_layout()
# plt.savefig(os.path.join(folder_name, "equi_width_histogram.png"))
# plt.show()
#

# Equal-depth Histogram:

depth_display_labels = []
current_index = 0
equi_depth_results = []

for i in range(num_bins):
    if i < remainder:
        this_bin_count = bin_size + 1  # Οι πρώτοι κάδοι παίρνουν το "έξτρα" άτομο
    else:
        this_bin_count = bin_size
    first_index = current_index
    last_index = current_index + this_bin_count - 1

    age_start = sorted_ages[first_index]
    age_end = sorted_ages[last_index]

    bracket = "]" if i == num_bins - 1 else ")"
    current_label = f"[{age_start}-{age_end}{bracket}"

    depth_display_labels.append(current_label)
    equi_depth_results.append((current_label, this_bin_count))
    current_index += this_bin_count

# plt.figure(figsize=(12, 6))
# depth_counts = [b[2] for b in equi_depth_bins]
#
# bars=plt.bar(range(num_bins), depth_counts, color='salmon', edgecolor='black', alpha=0.8)
# for i, bar in enumerate(bars):
#     height = bar.get_height()
#     plt.text(bar.get_x() + bar.get_width()/2., height + 5,f'{int(height)}',ha='center', va='bottom', fontsize=10, fontweight='bold')
# plt.title('Equi-depth Histogram')
# plt.xlabel('Age Ranges')
# plt.ylabel('Frequency')
# plt.xticks(range(num_bins), depth_display_labels, rotation=0) # Αλλαγή σε 0 για ίσια γράμματα
# plt.grid(axis='y', linestyle='--', alpha=0.5)
# plt.tight_layout()
# plt.savefig(os.path.join(folder_name, "equi_depth_histogram.png"))
# plt.show()

#------------------------------------------------------#
#                 EXPORT TO TXT                        #
#------------------------------------------------------#
output_file = "histogram_results.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("DAFERMOU CHRISTINA DANAE - 5206\n")
    f.write("VALERAS CHRISTOS - 5182\n\n")
    f.write("-" *10 +"HISTOGRAMS RESULTS:"+"-"*10+"\n\n")
    f.write("EQUI-WIDTH HISTOGRAM DATA:\n\n")
    f.write(f"{'Age Range':<15} | {'Frequency':<10}\n")
    f.write("-" * 30 + "\n")

    for w_lbl, w_cnt in zip(width_labels, bin_counts):
        f.write(f"{str(w_lbl):<15} | {str(w_cnt):<10}\n")

    f.write("\n\n")

    f.write("EQUI-DEPTH HISTOGRAM DATA:\n\n")
    f.write(f"{'Age Range':<15} | {'Frequency':<10}\n")
    f.write("-" * 30 + "\n")

    for item in equi_depth_results:
        range_text = item[0]
        freq_value = item[1]
        f.write(f"{range_text:<15} | {freq_value:<10}\n")

print(f"Results exported to '{output_file}'.")