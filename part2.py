#DAFERMOU CHRISTINA DANAE - 5206
#VALERAS CHRISTOS - 5182
import sys


# ===========================================================================================
# PART 2.1: SEMIJOIN AND ANTI-SEMIJOIN (Sort-Merge and Hash-Based Approaches)
# ===========================================================================================
# Reads a file and returns a list of tuples
# Skips empty lines and comment lines


def load_relation(filename):
    relation = []
    with open(filename, 'r',encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # xorizei me koma, vgazei eisagogika
                fields = [field.strip().strip('"') for field in line.split(',')]
                relation.append(tuple(fields))
    return relation

# ========================================================================================
# SORT-MERGE SEMIJOIN
# ========================================================================================
# Performs semijoin using the sort-merge approach
# Returns the tuples of relation R that have a match in relation S


def sort_merge_semijoin(r, s, join_idx_r=0, join_idx_s=0):
    # metatrepei se int an mporei, alliws afinei ws exei
    def to_int_key(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return val
   
    # sort kai ta 2
    r_sorted = sorted(r, key=lambda t: to_int_key(t[join_idx_r]))
    s_sorted = sorted(s, key=lambda t: to_int_key(t[join_idx_s]))
   
    result = []
    i = 0 # deiktis R
    j = 0 # deiktis S
   
    # klasiko sort-merge, mono krataei apo R
    while i < len(r_sorted) and j < len(s_sorted):
        key_r = to_int_key(r_sorted[i][join_idx_r])
        key_s = to_int_key(s_sorted[j][join_idx_s])
       
        if key_r < key_s:
            i += 1
        elif key_r > key_s:
            j += 1
        else:
            # match -> prosthese ola ta R me auto to key
            current_key = key_r
            while i < len(r_sorted) and to_int_key(r_sorted[i][join_idx_r]) == current_key:
                result.append(r_sorted[i])
                i += 1
            # skip ta idia keys sto S
            while j < len(s_sorted) and to_int_key(s_sorted[j][join_idx_s]) == current_key:
                j += 1
    return result
# =============================================
# HASH SEMIJOIN
# =============================================
# Implements semijoin using hashing, following a simpler approach


def hash_semijoin(r, s, join_idx_r=0, join_idx_s=0):
    # set me ta keys tou S
    s_keys = {tuple_row[join_idx_s] for tuple_row in s}
    # krata mono osa R exoun key sto S
    result = [tuple_row for tuple_row in r if tuple_row[join_idx_r] in s_keys]
    return result

# ===========================================================================================
# ANTI-SEMIJOIN
# ===========================================================================================
# The inverse operation of semijoin – returns tuples that do NOT have a match

def sort_merge_antisemijoin(r, s, join_idx_r=0, join_idx_s=0):
    semi = sort_merge_semijoin(r, s, join_idx_r, join_idx_s)
    semi_set = set(semi)
    return [t for t in r if t not in semi_set]

# idio me hash
def hash_antisemijoin(r, s, join_idx_r=0, join_idx_s=0):
    semi = hash_semijoin(r, s, join_idx_r, join_idx_s)
    semi_set = set(semi)
    return [t for t in r if t not in semi_set]


# ===========================================================================================
# TEST ME MIKRO PARADEIGMA
# ===========================================================================================


print("=== TEST WITH SMALL EXAMPLE ===")
test_r = [(1,2), (1,4), (2,5)]
test_s = [(1,'a'), (1,'c'), (3,'a')]
print("sort_merge_semijoin :", sort_merge_semijoin(test_r, test_s))


# ===========================================================================================
# FORTOSI DEDOMENON
# ===========================================================================================
airports = load_relation('airports.dat')
routes = load_relation('routes.dat')


# ===========================================================================================
# MEROS 2.2 - TELIKO PROGRAMMA
# ===========================================================================================


if len(sys.argv) == 2:
    aircraft_type = sys.argv[1].strip().upper()
    print(f"\n=== SEARCHING AIRPORTS FOR AIRCRAFT TYPE: {aircraft_type} ===")
 
    # krataei mono routes me to sigkekrimeno aeroskafos kai egkiro airport id
    selected_routes = [
        route for route in routes
        if route[5] != '\\N' and
        aircraft_type in [eq.strip() for eq in route[-1].split()]
    ]
 
    # sort me vasi airport id
    selected_sorted = sorted(selected_routes, key=lambda r: int(r[5]))
 
    # semijoin gia na vroume ta aerodromia
    matching_airports = sort_merge_semijoin(airports, selected_sorted, 0, 5)
 
    print(f"Found {len(matching_airports)} airports")
 
    # elegxos me hash - prepei na dinei to idio
    matching_hash = hash_semijoin(airports, selected_sorted, 0, 5)
    print(f"Hash version gives: {len(matching_hash)} airports")
 
    # print apotelesmata
    #for airport in matching_airports:
        #print(airport)
else:
    print("\n=== USAGE INSTRUCTIONS ===")
    print(" python3 assignment2.py SU9")
    print(" python3 assignment2.py 737")
    print(" python3 assignment2.py CR2")



# ===========================================================================================
# PART 2.3: PIPELINED MERGE JOIN + THREE-WAY SORT-MERGE JOIN
# ===========================================================================================
# Assumes that relations r, s, and t are already sorted based on attribute A (index 0)

# ===========================================================================================
# HELPER FUNCTION: 2-WAY FULL SORT-MERGE JOIN
# ===========================================================================================
# Implements the standard sort-merge join for two relations
# Uses pointers and grouping to avoid unnecessary repeated comparisons

def sort_merge_join_2way(r, s):
    result = []
    i = 0
    j = 0
    while i < len(r) and j < len(s):
        key_r = r[i][0]
        key_s = s[j][0]
        if key_r < key_s:
            i += 1
        elif key_r > key_s:
            j += 1
        else:
            current_key = key_r
            r_group = []
            while i < len(r) and r[i][0] == current_key:
                r_group.append(r[i])
                i += 1
            s_group = []
            while j < len(s) and s[j][0] == current_key:
                s_group.append(s[j])
                j += 1
            # cartesian product gia to matching group
            for rt in r_group:
                for st in s_group:
                    result.append((current_key, rt[1], st[1]))
    return result

# ===========================================================================================
# PIPELINED MERGE JOIN
# ===========================================================================================
# Computes join(r, s) and then joins the result with t
# without storing any intermediate results to disk (pipelining)

# Step 1: join r and s → rs(A, B, C)
# Step 2: join rs with t → (A, B, C, D)


def pipelined_merge_join(r, s, t):

    rs = sort_merge_join_2way(r, s)
    result = []
    i = 0
    j = 0
    while i < len(rs) and j < len(t):
        key_rs = rs[i][0]
        key_t = t[j][0]
        if key_rs < key_t:
            i += 1
        elif key_rs > key_t:
            j += 1
        else:
            current_key = key_rs
            rs_group = []
            while i < len(rs) and rs[i][0] == current_key:
                rs_group.append(rs[i])
                i += 1
            t_group = []
            while j < len(t) and t[j][0] == current_key:
                t_group.append(t[j])
                j += 1
            for rs_tup in rs_group:
                for tt in t_group:
                    result.append((current_key, rs_tup[1], rs_tup[2], tt[1]))
    return result

# ===========================================================================================
# THREE-WAY SORT-MERGE JOIN
# ===========================================================================================
# Performs a concurrent sort-merge join across all three relations
# Produces the final result F(A, B, C, D) directly, without any intermediate results

def three_way_sort_merge_join(r, s, t):
    result = []
    i = j = k = 0
    while i < len(r) and j < len(s) and k < len(t):
        kr = r[i][0]
        ks = s[j][0]
        kt = t[k][0]
       
        if kr == ks == kt:
            current_key = kr
            # collect groups
            r_group = []
            while i < len(r) and r[i][0] == current_key:
                r_group.append(r[i])
                i += 1
            s_group = []
            while j < len(s) and s[j][0] == current_key:
                s_group.append(s[j])
                j += 1
            t_group = []
            while k < len(t) and t[k][0] == current_key:
                t_group.append(t[k])
                k += 1
            # cartesian r x s x t
            for rt in r_group:
                for st in s_group:
                    for tt in t_group:
                        result.append((current_key, rt[1], st[1], tt[1]))
        else:
            # advance ola ta pointers pou exoun to mikrotero key
            min_key = min(kr, ks, kt)
            if kr == min_key:
                i += 1
            if ks == min_key:
                j += 1
            if kt == min_key:
                k += 1
    return result

# ===========================================================================================
# TEST ME TO PARADEIGMA TIS EKFONISIS 
# ===========================================================================================
print("=== TEST FOR PART 2.3 ===")
test_r = [(1,'b1'),(2,'b2'),(3,'b3'),(4,'b4')]
test_s = [(1,'c1'),(1,'c2'),(2,'c3'),(3,'c4')]
test_t = [(1,'d1'),(2,'d2'),(3,'d3'),(5,'d4')]

print("pipelined_merge_join  :", pipelined_merge_join(test_r, test_s, test_t))
print("three_way_sort_merge_join :", three_way_sort_merge_join(test_r, test_s, test_t))
