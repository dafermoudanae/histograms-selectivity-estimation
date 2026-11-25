# histograms-selectivity-estimation

Equi-width and equi-depth histograms for estimating the result size of selection queries, using internet usage data. Also includes semijoin and anti-semijoin implementations (sort-merge and hash-based) on airport and route data.

Assignment 1, Data Management (Διαχείριση Σύνθετων Δεδομένων), University of Ioannina, 2025-26.

## Contents
- `part1_1.py`: builds equi-width and equi-depth histograms on the Age attribute of `final_general.dat`, and exports them.
- `part1_2.py`: reads a range [a, b] from the user, estimates the number of records in that range with both histograms, and compares the estimates to the real count.
- `part2.py`: semijoin and anti-semijoin of `airports.dat` and `routes.dat`, using sort-merge and hash-based approaches.
- `final_general.dat`, `airports.dat`, `routes.dat`: input data.
-  `experiments_results.txt`, `histogram_results.txt`, `equi_width_histogram.png`, `equi_depth_histogram.png`: experiment results and histogram plots.

## Requirements
- Python 3
- Standard library only (matplotlib is only needed for the commented-out plotting code)

## How to Run
1. Clone the repository: `git clone https://github.com/dafermoudanae/histograms-selectivity-estimation.git`
2. Run from inside the project folder, since the scripts read the data files from the current directory:
   - Histograms: `python part1_1.py`
   - Range estimation: `python part1_2.py` (enter the values a and b when asked)
   - Semijoins: `python part2.py`
