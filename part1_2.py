# DAFERMOU CHRISTINA DANAE - 5206
# VALERAS CHRISTOS - 5182

#import matplotlib.pyplot as plt
import os

# folder_name = "histograms"
# os.makedirs(folder_name, exist_ok=True)

# ===========================================================================================
# Data Loading and Input Validation
# The program reads age values from the file "final_general.dat" and stores them in a list.
# It then determines the valid range of ages (min and max).
# The user is prompted to enter values a and b, ensuring they lie within this range.
# ===========================================================================================
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
#print("All ages from file:", ages)

min_age = min(ages)
max_age = max(ages)

while True:
    print("\n" + "-"*50)
    print("New experiment:")

    while True:
        a_val = float(input(f"Please enter number a: "))
        if a_val < min_age or a_val > max_age:
            print(f" {a_val} is out of range. Please enter a value between {min_age} and {max_age}.")
        else:
            break

    while True:
        b_val = float(input(f"Please enter number b: "))
        if b_val < min_age or b_val > max_age:
            print(f" {b_val} is out of range. Please enter a value between {min_age} and {max_age}")
        else:
            break


    a = min(a_val, b_val)
    b = max(a_val, b_val)
    num_bins = 10
    total_elements = len(ages)
    #print("total ages:",total_elements)

# ===========================================================================================
# Equi-Width Histogram Construction and Range Estimation
# The code builds an equi-width histogram by dividing the age range into equal bins.
# It counts how many values fall into each bin.
# Ιt estimates the number of elements within the interval [a, b]
# by computing the overlap between the query range and each bin,
# using linear interpolation based on the proportion of overlap.
# ===========================================================================================

    bin_width = (max_age - min_age) / num_bins
    bin_counts = [0] * num_bins

    for age in ages:
        idx = int((age - min_age) / bin_width)
        if idx == num_bins:
            idx = num_bins - 1
        bin_counts[idx] += 1
   # print(f"Bin counts for the Equi-width histogram: {bin_counts}")

#--------------------------------------estimation------------------------------------------#

    range_values = 0


    for i in range(num_bins):
        age_start = min_age + i * bin_width
        age_end = min_age + (i + 1) * bin_width

        #star of overlap:
        if a > age_start:
            start = a
        else:
            start = age_start

        #end of overlap:
        if b < age_end:
            end = b
        else:
            end = age_end

        if end > start:
            overlap = end - start
            proportion = overlap / bin_width
            range_values += proportion * bin_counts[i]

    # ===========================================================================================
    # Equi-Depth Histogram Construction and Range Estimation
    # The code constructs an equi-depth histogram by sorting the data and dividing it
    # into bins that contain (approximately) the same number of elements.
    # It determines the boundaries of each bin based on the sorted values.
    # Ιt estimates the number of elements within the interval [a, b]
    # by calculating the overlap between the query range and each bin,
    # using linear interpolation based on the proportion of overlap.
    # ===========================================================================================

    sorted_ages = sorted(ages)
    bin_size = total_elements // num_bins
    remainder = total_elements % num_bins

    current_index = 0
    equi_depth_sum = 0
    equi_depth_bins = []
    display_boundaries = []

    for i in range(num_bins):
        if i < remainder:
            this_bin_count = bin_size + 1
        else:
            this_bin_count = bin_size

        age_start = sorted_ages[current_index]
        age_end = sorted_ages[current_index + this_bin_count - 1]

        bracket = "]" if i == num_bins - 1 else ")"
        bin_label = f"[{age_start}-{age_end}{bracket}"

        equi_depth_bins.append((age_start, age_end, this_bin_count))
# -----------------------------------------estimation-------------------------------------------#

        start_overlap = max(a, age_start)
        end_overlap = min(b, age_end)



        if start_overlap <= end_overlap:
            overlap_range = end_overlap - start_overlap
            bin_range = age_end - age_start

            if bin_range > 0:
                proportion = overlap_range / bin_range
                equi_depth_sum += proportion * this_bin_count
            else:
                if a <= age_start <= b:
                    equi_depth_sum += this_bin_count
        current_index += this_bin_count


#-----------------------------------   ---real count------------------------------------------#
    real_count = 0
    for age in ages:
        if a <= age <= b:
            real_count += 1

    print(f"\nRESULTS FOR RANGE [{a}, {b}]:")
    print(f"1. Equi-width Estimate: {range_values:.2f}")
    print(f"2. Equi-depth Estimate: {equi_depth_sum:.2f}")
    print(f"3. Real Data Count:    {real_count}")


# ===========================================================================================
# Histogram Experiments
# For different values of parameters a and b, we conducted experiments in order to observe
# which histogram is closer to the real count.
# The results were stored in the file "experiments_results.txt".
# ===========================================================================================


    error_width = abs(range_values - real_count)
    error_depth = abs(equi_depth_sum - real_count)

    print(f"\nExperimental Results for range: [{a}-{b}] ")
    #print(f"Real Number of people: {real_count}")

    print(f"\nError of Equi-width: {error_width:.2f}")
    print(f"Error of Equi-depth: {error_depth:.2f}")

    if error_depth < error_width:
        print("\nEqui-depth is more accurate for this range.")
    else:
        print("\nEqui-width is more accurate for this range.")





    log_file = "experiments_results.txt"

    rel_error_width = (error_width / real_count * 100) if real_count > 0 else 0
    rel_error_depth = (error_depth / real_count * 100) if real_count > 0 else 0

    if rel_error_depth < rel_error_width:
        winner = "Equi-Depth"
    else:
        winner = "Equi-Width"

    score_width = 0
    score_depth = 0

    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in reversed(lines):
                if "SCORE:" in line:
                    try:

                        data_part = line.replace("SCORE:", "").strip()
                        parts = data_part.split("|")

                        score_width = int(parts[0].split(":")[1].strip())
                        score_depth = int(parts[1].split(":")[1].strip())
                        break
                    except (ValueError, IndexError):
                        continue
    if winner == "Equi-Width":
        score_width += 1
    else:
        score_depth += 1


    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("Histogram Experiments:\n")
            f.write("\n")

        f.write(f"New experiment:")
        f.write(f"For range: [{a:.1f} - {b:.1f}] | Real Count: {real_count}\n")
        f.write("\n")
        f.write(f"Equi-Width Error: {rel_error_width:.2f}%\n")
        f.write(f"Equi-Depth Error: {rel_error_depth:.2f}%\n")
        f.write("\n")
        f.write(f"Winner of round: {winner}\n")
        f.write(f"SCORE: Equi-Width: {score_width} | Equi-Depth: {score_depth}\n")
        f.write("-" * 40 + "\n")

    print(f"SCORE: Width {score_width} - Depth {score_depth}")
    cont = input("\nDo you want to do another experiment? (y/n): ").lower()
    if cont != 'y':
        print("End of experiments. Check the file 'experiments_results.txt' for the score!")



#------------------------------------------------------#
#                 MATLAB EXPORT                        #
#------------------------------------------------------#

# folder_name = "histograms"
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
    #
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

    # Equal-depth Histogram:

    depth_display_labels = []
    current_index = 0

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
        depth_display_labels.append(f"[{age_start}-{age_end}{bracket}")

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
    # break