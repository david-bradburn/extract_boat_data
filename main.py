
import pandas as pd

contacts_src = "src\contacts26.csv"
boats_src = "src\\boats26.csv"

df_contacts = pd.read_csv(contacts_src)
df_boats = pd.read_csv(boats_src)

valid_ids = []

def check_if_in_array(arr: list, item):
  if item in arr:
    raise Exception(f"uid: {item} already in list")
  else:
    return False

for index, row in df_contacts.iterrows():
  assert(row["membership_status"] == "Active")
  uid = row["uid"]
  if not check_if_in_array(valid_ids, uid):
    valid_ids.append(row["uid"])

# print(valid_ids)
count = 0

header = "Name, LOA, Beam, Vessel Type, Design, Sail Number, Designer\n"
fd = open("out.csv", "w")
fd.write(header)

for index, row in df_boats.iterrows():
  con_id = row["Contact IDs"]
  boat_name = row["Name"]
  boat_loa = row["LOA"]
  boat_beam = row["Beam"]
  boat_vtype = row["Vessel Type"]
  boat_design = row["Design"]
  boat_sailno = row["Sail Number"]
  boat_designer = row["Designer"]


  assert(len(con_id) > 0)
  for id in con_id.split("/"):
    if int(id) not in valid_ids:
      continue
    count += 1
    boat_data = f"{boat_name}, {boat_loa}, {boat_beam}, {boat_vtype}, {boat_design}, {boat_sailno}, {boat_designer}"
    # print(f"{boat_name} {boat_loa} {boat_beam} {boat_vtype} {boat_design} {boat_sailno} {boat_designer}")
    fd.write(f"{boat_data}\n")
    break
  else:
    print("Boat not active")

fd.close()

