## **Data Models:**

### **User**
`id` --- Auto-Generated, unique=True
email --- СharField or EmailField, unique=True
username --- СharField, unique=True
password --- СharField, type=Password
is_superuser --- Boolean, default=False
is_staff --- Boolean, default=False
is_active --- Boolean, default=False
is_verified --- Boolean, default=False


### **Company**
id --- Auto-Generated, unique=True
name --- СharField or EmailField, unique=True
description --- TextField, null+True, blank=True
admin_id --- Integer (FK link to User model)


### **Client**
id --- Auto-Generated, unique=True
user_id --- Integer (FK link to User model)
vip_status_id --- Integer (FK link to VipStatus model)
---
nickname --- СharField, unique=True
first_name --- CharField, => upperCase
last_name --- CharField, => uppercase
age --- Integer
country --- CharField, => uppercase
address --- CharField
phones --- CharField
note --- CharField


### **Coach**
id --- Auto-Generated, unique=True
user_id --- Integer (FK link to User model)
---
nickname --- СharField, unique=True
first_name --- CharField, => uppercase
last_name --- CharField, => uppercase
country --- CharField, => uppercase
address --- CharField
phones --- CharField
note --- CharField
---
specialities- Integer (FK link to Speciality model)


### **CoachSpeciality**
id --- Auto-Generated, unique=True
name --- name --- СharField, unique=True
description --- TextField, null+True, blank=True


### **VipStatus**
id --- Auto-Generated, unique=True
name --- name --- СharField, unique=True
description --- TextField, null+True, blank=True


### **MoodCategory**
id --- Auto-Generated, unique=True
name --- name --- СharField, unique=True
description --- TextField, null+True, blank=True


### **Group**
id --- Auto-Generated, unique=True
name --- СharField, unique=True
description --- TextField, null+True, blank=True
start_date --- DateTimeField
finish_date --- DateTimeField, null=True, blank=True


### **Dynamics**
id --- Auto-Generated, unique=True
user_id --- Integer (FK link to User model)
group_id --- Integer (FK link to Group model)
mood_id --- Integer (FK link to MoodCategory model)
date --- DateField, required=True
current_weight --- DecimalField
current_breast_size --- DecimalField
current_waist_size --- DecimalField
current_hip_size --- DecimalField


#### **For the future:**
weight_unit --- Integer (FK link to WeightUnit model)
water_unit --- Integer (FK link to WaterUnit model)
fat_unit --- Integer (FK link to FatUnit model)
size_unit --- Integer (FK link to FatUnit model)



#### **WeightUnit**
id --- Auto-Generated, unique=True
brief_name --- СharField, unique=True
name --- СharField, unique=True
units_per_kg --- DecimalField, required = True

#### **WaterUnit**
id --- Auto-Generated, unique=True
brief_name --- СharField, unique=True
name --- СharField, unique=True
units_per_litre --- DecimalField, required = True


#### **FatUnit**
id --- Auto-Generated, unique=True
brief_name --- СharField, unique=True
name --- СharField, unique=True
units_per_kg (???) --- DecimalField, required = True


#### **SizeUnit**
id --- Auto-Generated, unique=True
brief_name --- СharField, unique=True
name --- СharField, unique=True
units_per_meter --- DecimalField, required = True
