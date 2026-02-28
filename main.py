
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

contacts_src = "src\contacts26.csv"
boats_src = "src\\boats26.csv"

df_contacts = pd.read_csv(contacts_src)
df_boats = pd.read_csv(boats_src)

contacts_dict = {}

def check_if_in_dict(contacts_dict: dict, item):
  if item in contacts_dict:
    raise Exception(f"uid: {item} already in dict")
  else:
    return False

m_dict = {"Ordinary": "O",
          "Ordinary H/R": "O",
          "Ordinary Family": "OF",
          "Ordinary Family H/R": "OF",
          "Associate": "A",
          "Associate H/R": "A",
          "Associate Family": "A/F",
          "Associate Family H/R": "A/F",
          "Cadet": "Cdt",
          "Country": "C",
          "Country Family": "CF",
          "Life": "L",
          "Honorary": "H",
          "Student": "S"}

header_members = "Membership Started, First Name, Surname, Membership Type, Boat Name, City, County, Phone Number\n"
fd_mem = open("members.csv", "w")
fd_mem.write(header_members)

for index, row in df_contacts.iterrows():
  assert(row["membership_status"] == "Active")
  uid = row["uid"]
  fname = row["first_name"]
  sname = row["last_name"]
  mtype = row["membership_types"]
  bname = row["boat_name"]
  city = row["city"]
  county = row["county"]
  memstart = row["membership_started"]

  mnum = row["phone"] if row["mobile"] == "nan" or row["mobile"] == "" else row["mobile"]
  year_started = memstart.split("/")[2]
  # dt_memstart = datetime.strptime(memstart, '%d/%M/%Y')
  # today = datetime.today()

  # print(relativedelta(today, dt_memstart).years)
  # print(memstart)
  if mtype not in m_dict:
    translated_mtype = ""
    print(f"[WARNING] Member {fname} {sname} has invalid membership type of {mtype}")
  else:
    translated_mtype = m_dict[mtype]

  if not check_if_in_dict(contacts_dict, uid):
    contacts_dict[uid] = [fname, sname, translated_mtype, bname, city, county, str(mnum)]

  fd_mem.write(f"{year_started}, {fname}, {sname}, {translated_mtype}, {bname}, {city}, {county}\n")
fd_mem.close()
# print(valid_ids)
count = 0

header_boat = "Name, LOA, Beam, Vessel Type, Design, Sail Number, Designer, Owners Name (s)\n"
fd = open("boats.csv", "w")
fd.write(header_boat)

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
  is_valid = False
  tmp_owners_names = []

  for id in con_id.split("/"):
    if int(id) not in contacts_dict:
      continue
    count += 1
    is_valid =  True
    # print(contacts_dict.values())
    # , " + ", ".join(
    # print(f"{boat_name} {boat_loa} {boat_beam} {boat_vtype} {boat_design} {boat_sailno} {boat_designer}")
    owner_name = f"{contacts_dict[int(id)][0]} {contacts_dict[int(id)][1]}"
    tmp_owners_names.append(owner_name)

  if is_valid:
    boat_data = f"{boat_name}, {boat_loa}, {boat_beam}, {boat_vtype}, {boat_design}, {boat_sailno}, {boat_designer}, "  + "/ ".join(tmp_owners_names)
    fd.write(f"{boat_data}\n")


fd.close()

