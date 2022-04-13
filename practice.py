import datetime

created = "22.04.07"


created = created.replace(".", "")
created = "20" + created
created = datetime.datetime.strptime(created, "%Y%m%d").date()

print(created)