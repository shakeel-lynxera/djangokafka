from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
import pandas as pd

from audit_logs.models import AuditLogs
from djangokafka import settings
from django.db.utils import IntegrityError

from common.kafka.consumer import update_or_create_customer_feature_permission
from common.models import (
    CustomerProxy,
    CustomerPackageAllocationProxy,
    FleetProxy,
    FuelProxy,
    UserProxy,
    VehicleProxy,
    CustomerFeaturesAssociation,
    SystemFeaturesChoices,
)
from driver.models import Driver, DriverGroup, DriverVehilceAllocation
from shifts.models import Shift
from jobs.models import Job, Location
from tools.models import Tool

"""

INSERT INTO "common_packageproxy" ("created_at", "updated_at", "status", "package_id", "name", "no_of_users", "is_active") VALUES
('2022-09-22 01:17:13.863812+00',	'2022-09-22 01:17:13.863829+00',1,	8,	'Basic',	3,	'1'),
('2022-09-22 01:59:12.873226+00',	'2022-09-22 01:59:12.873244+00',1,	6,	'Advance',	5,	'1'),
('2022-10-10 09:39:00.056411+00',	'2022-10-10 09:39:00.056474+00',1,	9,	'Plug and Go',	4,	'1'),
('2022-09-23 12:29:14.700732+00',	'2022-09-23 12:29:14.700748+00',1,	7,	'Advance Plus',	9,	'1'),
('2022-09-22 03:13:18.07098+00',	'2022-09-22 03:13:18.070998+00',1,	10,	'Advance',	5,	'1'),
('2022-09-21 21:42:50.969195+00',	'2022-09-21 21:42:50.969215+00',1,	16,	'Basic',	6,	'1'),
('2022-10-06 11:53:02.227146+00',	'2022-10-06 11:53:02.227164+00',1,	5,	'Plug and Go',	3,	'1');

"""
path = f"{settings.BASE_DIR}/common/management/commands/files"


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        All migrations commands are written within this function
        """

        create_customers()
        customer_packages_associations()
        create_userproxies()
        create_fleets()
        create_vehilces()
        create_fuels()
        create_driver_groups()
        create_drivers()
        driver_vehicle_allocation()
        shifts_management()
        create_jobs()
        create_tools()
        audit_logs()


def create_customers():
    df = pd.read_csv(f"{path}/customer_customer.csv")
    df = df.fillna("")
    try:
        CustomerProxy.objects.all().delete()
        for row in df.values.tolist():
            if row[7] == 1:
                value = 1
            elif row[7] == 2:
                value = 0
            else:
                value = None
            customer = CustomerProxy.objects.create(
                created_at=row[3] if row[3] else None,
                updated_at=row[3] if row[3] else None,
                customer_id=row[0],
                name=row[1] if row[1] else None,
                email=row[12] if row[12] else None,
                is_active=value,
                timezone="Asia/Qatar",
                status=value,
            )
            customer.created_at = row[3]
            customer.save()
            update_or_create_customer_feature_permission(customer, True)
            CustomerFeaturesAssociation.objects.update_or_create(
                customer=customer,
                feature=SystemFeaturesChoices.DRIVER_APP,
                defaults={
                    "is_enabled": True,
                },
            )

        print("SUCCESS:- Customer Creations")
    except Exception as e:
        print("customer_customer", e)


def customer_packages_associations():
    try:
        CustomerPackageAllocationProxy.objects.all().delete()
        customers = CustomerProxy.objects.all()
        for customer in customers:
            CustomerPackageAllocationProxy.objects.create(
                customer=customer,
                package_id=16,
            )
        print("SUCCESS:- Customer Package Association")
    except Exception as e:
        print("customer_assignedusecasepackage", e)


def create_userproxies():
    df = pd.read_csv(f"{path}/user_profile_user_new.csv")
    df = df.fillna("")
    try:
        UserProxy.objects.all().delete()
        for row in df.values.tolist():
            try:
                customer = CustomerProxy.objects.filter(customer_id=row[24]).first()
                UserProxy.objects.create(
                    created_at=row[36] if row[36] else None,
                    updated_at=row[28] if row[28] else None,
                    guid=row[7] if row[7] else None,
                    first_name=row[2] if row[2] else None,
                    last_name=row[3] if row[3] else None,
                    username=row[10] if row[10] else None,
                    email=row[11] if row[11] else None,
                    department=row[30] if row[30] else None,
                    user_type=1,
                    status=1 if row[26] == 1 else 0,
                    phone=row[22] if row[22] else None,
                    is_active=row[5] if row[5] == 1 else 0,
                    data_joined=row[6] if row[6] else None,
                    work_location=row[34] if row[34] else None,
                    internal_role=row[35] if row[35] else None,
                    customer=customer if customer else None,
                )
            except Exception as err:
                print(err)
        print("SUCCESS:- User Proxies Creations.")
    except Exception as e:
        print(e)


def create_fleets():
    df = pd.read_csv(f"{path}/fleet.csv")
    df = df.fillna("")
    try:
        FleetProxy.objects.all().delete()
        for row in df.values.tolist():
            try:
                row[6] = int(row[6]) if row[6] else None
                customer = CustomerProxy.objects.filter(customer_id=row[6]).first()
                FleetProxy.objects.create(
                    created_at=row[3] if row[3] else None,
                    updated_at=row[4] if row[4] else None,
                    fleet_id=row[0],
                    fleet_name=row[1] if row[1] else None,
                    status=row[9] if row[9] else 0,
                    customer=customer if customer else None,
                )
            except Exception as err:
                print(err)

        print("SUCCESS:- Fleets Creation")

    except Exception as e:
        print(e)


def create_vehilces():
    df = pd.read_csv(f"{path}/vehicleproxynew.csv")
    df = df.fillna("")
    try:
        VehicleProxy.objects.all().delete()
        for row in df.values.tolist():

            vehicle_id = int(row[0]) if row[0] else None
            vehicle_name = str(row[1]) if row[1] else ""
            status_id = int(row[2]) if row[2] else row[2]
            device_id = row[3]
            fleet_id = get_value(row[4])
            customer_id = int(row[6]) if row[6] else None

            customer = CustomerProxy.objects.filter(customer_id=customer_id).first()
            if customer is None:
                continue

            fleet = FleetProxy.objects.filter(fleet_id=fleet_id).first()
            # if VehicleProxy.objects.filter(name=vehicle_name).exists():
            #     continue
            VehicleProxy.objects.update_or_create(
                id=vehicle_id,
                defaults={
                    "vehicle_id": vehicle_id,
                    "name": vehicle_name,
                    "status": status_id,
                    "customer": customer,
                    "fleet": fleet,
                    "device_id": device_id,
                },
            )
        print("SUCCESS:- Vehicle Creations")

    except Exception as e:
        print(e)


def create_fuels():
    df = pd.read_csv(f"{path}/iof_logisticsfuelfillup.csv")
    df = df.fillna("")
    try:
        FuelProxy.objects.all().delete()
        for row in df.values.tolist():
            row[14] = int(row[14]) if row[14] else None
            row[10] = int(row[10]) if row[10] else None
            customer = CustomerProxy.objects.filter(customer_id=row[14]).first()
            vehicle = VehicleProxy.objects.filter(vehicle_id=row[10]).first()
            if vehicle is None:
                continue
            FuelProxy.objects.create(
                created_at=row[8] if row[8] else None,
                updated_at=row[10] if row[10] else None,
                fuel_filled=row[1] if row[1] else None,
                amount_paid=row[2] if row[2] else None,
                driver_name=row[3] if row[3] else None,
                location=row[4] if row[4] else None,
                fuel_supervisor_name=row[5] if row[5] else None,
                customer=customer if customer else None,
                fill_up_date=row[6] if row[6] else None,
                vehicle=vehicle,
            )
        print("SUCCESS:- Fuel Creations")
    except Exception as e:
        print(e)


def create_driver_groups():
    df = pd.read_csv(f"{path}/hypernet_drivergroup.csv")
    df = df.fillna("")
    try:
        DriverGroup.objects.all().delete()
        for row in df.values.tolist():
            row[2] = int(row[2]) if row[2] else None
            user = UserProxy.objects.filter(customer__customer_id=row[2]).first()
            if not user:
                continue
            DriverGroup.objects.create(id=row[0], name=row[1], user=user)
        print("SUCCESS:- Driver Groups Creations")
    except Exception as err:
        print(err)


def create_drivers():
    import uuid

    df = pd.read_csv(f"{path}/drivers.csv")
    df = df.fillna("")
    try:
        UserProxy.objects.filter(user_type=4).delete()
        Driver.objects.all().delete()
        for row in df.values.tolist():

            status_id = int(row[109]) if row[109] else None
            if status_id in [0, 12, None]:
                continue

            row[22] = int(row[22]) if row[22] else None
            customer = CustomerProxy.objects.filter(customer_id=row[22]).first()
            modified_by = UserProxy.objects.filter(
                user_type="1", customer=customer
            ).first()
            if customer is None:
                continue

            full_name = row[40]
            fn, ln = split_full_name(full_name)

            user = UserProxy.objects.create(
                guid=str(uuid.uuid4()),
                first_name=fn,
                last_name=ln,
                username=row[30] if row[30] else None,
                password=make_password(row[5]) if row[5] else None,
                email=row[4] if row[4] else None,
                customer=customer if customer else None,
                user_type=4,
                phone=row[17] if row[17] else None,
                is_active=row[10] if row[10] else None,
                data_joined=row[8] if row[8] else None,
            )
            row[23] = int(row[23]) if row[23] else None
            if row[23] == 3:
                gender = "1"
            elif row[23] == 4:
                gender = "2"
            else:
                gender = "3"

            row[103] = int(row[103]) if row[103] else None
            if row[103] == 8:
                marital_status = "1"
            elif row[103] == 9:
                marital_status = "2"
            else:
                marital_status = "3"

            row[39] = row[39]
            row[63] = str(row[63]) if row[63] else None
            driver = Driver.objects.create(
                id=row[39],
                name=full_name,
                salary=row[66] if row[66] else None,
                employee_id=row[63],
                dob=row[58] if row[58] else None,
                marital_status=marital_status,
                gender=gender,
                poi=row[115] if row[115] else False,
                user=user,
                pop_up_notification=row[31] if row[31] else False,
                status=status_id,
                modified_by=modified_by,
            )
            driver.created_at = row[8]
            driver.save()
            row[117] = int(row[117]) if row[117] else None
            if not row[117]:
                continue
            if not DriverGroup.objects.filter(id=row[117]).exists():
                continue
            driver.driver_group_association.create(driver_group_id=row[117])
        print("SUCCESS:- Driver Creation and Driver Groups Association")
    except Exception as err:
        print(err)


def driver_vehicle_allocation():
    df = pd.read_csv(f"{path}/drivervehicleproxy.csv")
    df = df.fillna("")
    try:
        DriverVehilceAllocation.objects.all().delete()
        for row in df.values.tolist():
            row[10] = int(row[10]) if row[10] else 12
            if row[10] == 1:
                status = 1
            else:
                status = 0

            row[2] = int(row[2]) if row[2] else None
            row[4] = int(row[4]) if row[4] else None
            row[3] = int(row[3]) if row[3] else None
            row[11] = int(row[11]) if row[11] else None
            customer = CustomerProxy.objects.filter(customer_id=row[2]).first()
            if customer is None:
                continue

            if not row[4] or not row[11]:
                continue

            user = UserProxy.objects.filter(customer=customer).first()
            driver = Driver.objects.filter(id=row[4]).first()
            if driver is None:
                continue

            vehicle = VehicleProxy.objects.filter(id=row[11]).first()
            if vehicle is None:
                continue

            dva = DriverVehilceAllocation.objects.create(
                created_at=row[1] if row[1] else None,
                updated_at=row[1] if row[1] else None,
                status=status,
                start_date=row[9].split(" ")[0] if row[9] else None,
                end_date=row[8].split(" ")[0] if row[8] else None,
                driver=driver,
                vehicle=vehicle,
                user=user,
            )
            dva.created_at = row[1]
            dva.save()
        DriverVehilceAllocation.objects.filter(status=0).delete()
        print("SUCCESS:- Driver Vehicle association")
    except Exception as e:
        print(e)


def shifts_management():
    df = pd.read_csv(f"{path}/shiftproxy.csv")
    df = df.fillna("")
    try:
        Shift.objects.all().delete()
        for row in df.values.tolist():
            row[2] = get_value(row[2])
            status = int(row[37]) if row[37] else 0
            if status in [0, 12]:
                continue
            user = UserProxy.objects.filter(customer__customer_id=row[2]).first()
            if Shift.objects.filter(name=get_value(row[15])).exists():
                shift = Shift.objects.filter(name=get_value(row[15])).first()
            else:
                shift = Shift.objects.create(
                    name=get_value(row[15]),
                    start_date=get_value(row[16]),
                    end_date=get_value(row[17]),
                    shift=get_value(row[38]),
                    user=user,
                    status=status,
                )
                shift.created_at = row[1]
                shift.save()
                shift.shift_timing.create(
                    day="monday",
                    start_time=get_value(row[19]),
                    end_time=get_value(row[20]),
                )
                shift.shift_timing.create(
                    day="tuesday",
                    start_time=get_value(row[21]),
                    end_time=get_value(row[22]),
                )
                shift.shift_timing.create(
                    day="wednesday",
                    start_time=get_value(row[23]),
                    end_time=get_value(row[24]),
                )
                shift.shift_timing.create(
                    day="thursday",
                    start_time=get_value(row[25]),
                    end_time=get_value(row[26]),
                )
                shift.shift_timing.create(
                    day="friday",
                    start_time=get_value(row[27]),
                    end_time=get_value(row[28]),
                )
                shift.shift_timing.create(
                    day="saturday",
                    start_time=get_value(row[29]),
                    end_time=get_value(row[30]),
                )
                shift.shift_timing.create(
                    day="sunday",
                    start_time=get_value(row[31]),
                    end_time=get_value(row[32]),
                )

                shift.shift_timing.filter(
                    start_time__isnull=True, end_time__isnull=True
                ).delete()

            if not Driver.objects.filter(id=get_value(row[4])).exists():
                continue

            allocation_status = int(row[10]) if row[10] else 0
            if allocation_status in [0, 12]:
                continue

            shift.driver_shift_allocation.create(
                driver_id=get_value(row[4]),
                start_date=get_value(row[9]),
                end_date=get_value(row[8]),
                user=user,
                status=allocation_status,
            )
        print("SUCCESS:- Shifts and Driver Shift Associations")
    except Exception as err:
        print(f"Error 'Shift Management':- {err}")


def create_jobs():
    df = pd.read_csv(f"{path}/job.csv")
    df = df.fillna("")
    Job.objects.all().delete()
    try:
        for row in df.values.tolist():
            status = int(row[57]) if row[57] else 0
            if status in [0, 12]:
                continue
            row[52] = int(row[52]) if row[52] else 1
            if row[52] == 52:
                job_status = 2
            elif row[52] == 53:
                job_status = 1
            elif row[52] == 54:
                job_status = 4
            elif row[52] == 55:
                job_status = 3
            else:
                job_status = 1

            row[52] = int(row[52]) if row[52] else 1
            if row[52] == 52:
                task_status = 2
            elif row[52] == 53:
                task_status = 1
            elif row[52] == 54:
                task_status = 4
            elif row[52] == 55:
                task_status = 3
            else:
                task_status = 1

            # row[20] = int(row[20]) if row[20] else 1
            # if row[20] == 52:
            #     task_status = 2
            # elif row[20] == 53:
            #     task_status = 1
            # elif row[20] == 54:
            #     task_status = 4
            # elif row[20] == 55:
            #     task_status = 3
            # else:
            #     task_status = 1

            row[15] = int(row[15]) if row[15] else None
            driver = Driver.objects.filter(id=row[15]).first()
            user = UserProxy.objects.filter(customer__customer_id=row[12]).first()
            if Job.objects.filter(job_name=get_value(row[1])).exists():
                job = Job.objects.filter(job_name=get_value(row[1])).first()
            else:
                job = Job.objects.create(
                    id=get_value(row[0]),
                    job_name=get_value(row[1]),
                    start_date=get_value(row[3]),
                    end_date=get_value(row[4]),
                    start_time_by_driver=get_value(row[28]),
                    end_time_by_driver=get_value(row[29]),
                    job_type=1 if get_value(row[53]) == 215 else 2,
                    job_status=job_status,
                    driver=driver,
                    user=user,
                    violations=0,
                    distance=0,
                    speed=0,
                )
                job.created_at = row[6]
                job.save()

            try:
                latitude = str(get_value(row[96])).split(",")[0].split(":")[1]
            except Exception as err:
                print(f"WARNING: {err}")
                latitude = None

            try:
                longitude = (
                    str(get_value(row[96])).split(",")[1].split(":")[1].replace("}", "")
                )
            except Exception as err:
                print(f"WARNING: {err}")
                longitude = None

            if Location.objects.filter(
                address=get_value(row[92]), description=get_value(row[64])
            ).exists():
                pickup_location = Location.objects.filter(
                    address=get_value(row[92]), description=get_value(row[64])
                ).first()
            else:
                pickup_location = Location.objects.create(
                    address=get_value(row[92]),
                    latitude=latitude,
                    longitude=longitude,
                    description=get_value(row[64]),
                    user=user,
                )

            # Destination
            df2 = pd.read_csv(f"{path}/job2.csv")
            df2 = df2.fillna("")
            for row2 in df2.values.tolist():
                if row2[0] == row[0]:
                    try:
                        latitude = str(get_value(row[96])).split(",")[0].split(":")[1]
                    except Exception as err:
                        print(f"WARNING: {err}")
                        latitude = None

                    try:
                        longitude = (
                            str(get_value(row[96]))
                            .split(",")[1]
                            .split(":")[1]
                            .replace("}", "")
                        )
                    except Exception as err:
                        print(f"WARNING: {err}")
                        longitude = None

                    if Location.objects.filter(
                        address=get_value(row[92]), description=get_value(row[64])
                    ).exists():
                        dropoff_location = Location.objects.filter(
                            address=get_value(row[92]), description=get_value(row[64])
                        ).first()
                    else:
                        dropoff_location = Location.objects.create(
                            address=get_value(row2[92]),
                            latitude=latitude,
                            longitude=longitude,
                            description=get_value(row2[64]),
                            user=user,
                        )
                    break
            abort_reason = get_value(row[25])
            if abort_reason == 40:
                abort_reason = "Untraceable Address"
            elif abort_reason == 41:
                abort_reason = "Incomplete Address"
            elif abort_reason == 42:
                abort_reason = "Restricted Area"
            elif abort_reason == 43:
                abort_reason = "Closed"
            else:
                abort_reason = "Other"

            job.tasks.create(
                priority=get_value(row[2]),
                task_status=task_status,
                abort_reason=abort_reason,
                abort_reason_description=get_value(row[24]),
                start_date=get_value(row[28]),
                end_date=get_value(row[28]),
                pick_up=pickup_location,
                drop_off=dropoff_location,
            )

        print("SUCCESS:- Jobs, Tasks, Location and Jobs Assignment")
    except Exception as err:
        print(f"ERROR 'Jobs':- {err}")


def create_tools():
    df = pd.read_csv(f"{path}/tools.csv")
    df = df.fillna("")
    Tool.objects.all().delete()
    try:
        for row in df.values.tolist():
            id = int(row[0]) if row[0] else None
            customer_id = int(row[2]) if row[2] else None
            imei = str(row[1]) if row[1] else None
            make = str(row[3]) if row[3] else None
            model = str(row[4]) if row[4] else None
            vehicle_id = int(row[6]) if row[6] else None
            sim_number = str(row[5]) if row[5] else None
            created_at = str(row[7]) if row[7] else None

            user = UserProxy.objects.filter(customer__customer_id=customer_id).first()
            vehicle = VehicleProxy.objects.filter(id=vehicle_id).first()
            if vehicle is None:
                continue

            if Tool.objects.filter(imei=imei).exists():
                continue

            try:
                tool = Tool.objects.create(
                    id=id,
                    imei=imei,
                    vehicle=vehicle,
                    make=make,
                    model=model,
                    sim_number=sim_number,
                    user=user,
                )
                tool.created_at = created_at
                tool.save()
            except IntegrityError:
                print("WARNING:- Tool with IMEI already exists")
        print("SUCCESS:- Tools Creations")
    except Exception as err:
        print(f"ERROR 'Tools':- {err}")


def audit_logs():
    df = pd.read_csv(f"{path}/options_log.csv")
    df = df.fillna("")
    AuditLogs.objects.all().delete()
    try:
        for row in df.values.tolist():
            try:
                type_id = None
                action = None

                if row[5].lower() == "driver":
                    type_id = "1"
                elif row[5].lower() == "job":
                    type_id = "2"
                else:
                    continue

                if row[1].lower() == "create":
                    action = 1
                if row[1].lower() == "update":
                    action = 2
                if row[1].lower() == "delete":
                    action = 3

                user = UserProxy.objects.filter(email=row[4]).first()
                try:
                    audit = AuditLogs.objects.create(
                        entity=type_id,
                        status=1,
                        created_at=row[3],
                        updated_at=row[3],
                        action=action,
                        user=user,
                        action_detail=row[2] if row[2] else None,
                        action_by=user,
                    )
                    audit.created_at = row[3]
                    audit.updated_at = row[3]
                    audit.save()
                except Exception as e:
                    print(e)
                    pass
            except Exception as e:
                print(e)
                pass
        print("SUCCESS:- Audit Logs")
    except Exception as e:
        print(e)


def get_value(val):
    val = val if val else None
    return val


def split_full_name(full_name):
    if len(full_name.split(" ")) == 1:
        first_name = full_name.split(" ")[0]
        last_name = None
    if len(full_name.split(" ")) > 1:
        first_name = full_name.split(" ")[0]
        last_name = full_name.split(" ")[1]
    return first_name, last_name
