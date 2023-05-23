tp_per = 0
fp_per = 0
fn_per = 0

tp_org = 0
fp_org = 0
fn_org = 0

tp_loc = 0
fp_loc = 0
fn_loc = 0

with open(
    "./predictions.txt", "r"
) as output_file:
    outputs = output_file.readlines()

for line in outputs:
    splitted_line = line.replace("\n", "").split(" ")
    if len(splitted_line) > 2:
        if splitted_line[1] == "location":
            if splitted_line[2] == "location":
                tp_loc += 1
            else:
                fn_loc += 1
                if splitted_line[2] == "person":
                    fp_per += 1
                if splitted_line[2] == "organization":
                    fp_org += 1
        elif splitted_line[1] == "person":
            if splitted_line[2] == "person":
                tp_per += 1
            else:
                fn_per += 1
                if splitted_line[2] == "location":
                    fp_loc += 1
                if splitted_line[2] == "organization":
                    fp_org += 1
        elif splitted_line[1] == "organization":
            if splitted_line[2] == "organization":
                tp_org += 1
            else:
                fn_org += 1
                if splitted_line[2] == "person":
                    fp_per += 1
                if splitted_line[2] == "location":
                    fp_loc += 1
        elif splitted_line[2] == "organization":
            fp_org += 1
        elif splitted_line[2] == "person":
            fp_per += 1
        elif splitted_line[2] == "location":
            fp_loc += 1

print("TP LOC ", tp_loc)
print("FP LOC ", fp_loc)
print("FN LOC ", fn_loc)
p_loc = tp_loc / (fp_loc + tp_loc)
r_loc = tp_loc / (fn_loc + tp_loc)
f_loc = 2 * (p_loc * r_loc) / (p_loc + r_loc)
print("F-1 Loc : ", f_loc)


print("TP Per ", tp_per)
print("FP Per ", fp_per)
p_per = tp_per / (fp_per + tp_per)
r_per = tp_per / (fn_per + tp_per)
f_per = 2 * (p_per * r_per) / (p_per + r_per)
print("F-1 Per : ", f_per)

print("FN Per ", fn_per)
print("TP Org ", tp_org)
print("FP Org ", fp_org)
p_org = tp_org / (fp_org + tp_org)
r_org = tp_org / (fn_org + tp_org)
f_org = 2 * (p_org * r_org) / (p_org + r_org)
print("F-1 org : ", f_org)

print("F-1 macro : ", (f_org + f_per + f_loc) / 3)
print("F1 micro:", ()) 