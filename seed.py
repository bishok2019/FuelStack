#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session

from apps.authentication.models.roles_permissions import (
    CustomPermission,
    CustomRole,
    PermissionCategory,
)
from apps.authentication.models.users import User
from apps.authentication.utils import hash_password
from apps.database import SessionLocal, engine
from apps.dealers.models.brand import Brand
from apps.dealers.models.dealer import Dealer
from apps.dealers.models.hub import Hub
from apps.inventory.models import Inventory


def seed_data():
    db: Session = SessionLocal()

    try:
        # Clear existing data
        db.query(Inventory).delete()
        db.query(Hub).delete()
        db.query(Dealer).delete()
        db.query(Brand).delete()
        db.query(User).delete()
        db.query(CustomRole).delete()
        db.query(CustomPermission).delete()
        db.query(PermissionCategory).delete()
        db.commit()

        # Create permission categories
        cat_auth = PermissionCategory(name="Authentication")
        cat_inventory = PermissionCategory(name="Inventory")
        cat_dealers = PermissionCategory(name="Dealers")

        db.add_all([cat_auth, cat_inventory, cat_dealers])
        db.commit()

        # Create permissions
        permissions = [
            CustomPermission(
                name="View Users", code_name="can_view_users", category=cat_auth
            ),
            CustomPermission(
                name="Create Users", code_name="can_create_users", category=cat_auth
            ),
            CustomPermission(
                name="Edit Users", code_name="can_edit_users", category=cat_auth
            ),
            CustomPermission(
                name="Delete Users", code_name="can_delete_users", category=cat_auth
            ),
            CustomPermission(
                name="View Inventory",
                code_name="can_view_inventory",
                category=cat_inventory,
            ),
            CustomPermission(
                name="Create Inventory",
                code_name="can_create_inventory",
                category=cat_inventory,
            ),
            CustomPermission(
                name="Edit Inventory",
                code_name="can_edit_inventory",
                category=cat_inventory,
            ),
            CustomPermission(
                name="Delete Inventory",
                code_name="can_delete_inventory",
                category=cat_inventory,
            ),
            CustomPermission(
                name="View Dealers", code_name="can_view_dealers", category=cat_dealers
            ),
            CustomPermission(
                name="Create Dealers",
                code_name="can_create_dealers",
                category=cat_dealers,
            ),
            CustomPermission(
                name="Edit Dealers", code_name="can_edit_dealers", category=cat_dealers
            ),
            CustomPermission(
                name="Delete Dealers",
                code_name="can_delete_dealers",
                category=cat_dealers,
            ),
        ]

        db.add_all(permissions)
        db.commit()

        # Create roles
        admin_role = CustomRole(
            name="Admin", description="Administrator with full access"
        )
        manager_role = CustomRole(
            name="Manager", description="Manager with limited access"
        )
        user_role = CustomRole(name="User", description="Basic user")

        # Assign permissions to roles
        admin_role.permissions = permissions  # All permissions
        manager_role.permissions = [
            p for p in permissions if "delete" not in p.code_name
        ]  # No delete
        user_role.permissions = [
            p for p in permissions if p.code_name.startswith("can_view")
        ]  # Only view

        db.add_all([admin_role, manager_role, user_role])
        db.commit()

        # Create users
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            is_superuser=True,
        )
        manager_user = User(
            username="manager",
            email="manager@example.com",
            hashed_password=hash_password("manager123"),
        )
        basic_user = User(
            username="user",
            email="user@example.com",
            hashed_password=hash_password("user123"),
        )

        # Assign roles
        admin_user.user_roles = [admin_role]
        manager_user.user_roles = [manager_role]
        basic_user.user_roles = [user_role]

        db.add_all([admin_user, manager_user, basic_user])
        db.commit()

        # Create brands
        brand1 = Brand(name="PetrolCorp", code="PC", description="Leading petrol brand")
        brand2 = Brand(name="DieselMax", code="DM", description="Premium diesel brand")

        db.add_all([brand1, brand2])
        db.commit()

        # Create dealers
        dealer1 = Dealer(
            name="City Fuel Station",
            code="CFS",
            address="123 Main St, City Center",
            latitude="27.7172",
            longitude="85.3240",
            description="Central fuel station",
        )
        dealer2 = Dealer(
            name="Highway Fuel Hub",
            code="HFH",
            address="456 Highway Rd",
            latitude="27.7000",
            longitude="85.3300",
            description="Highway fuel hub",
        )

        db.add_all([dealer1, dealer2])
        db.commit()

        # Create hubs
        hub1 = Hub(
            name="Downtown Hub",
            code="DH",
            address="Downtown Area",
            latitude="27.7172",
            longitude="85.3240",
            description="Downtown distribution hub",
            dealer=dealer1,
        )
        hub2 = Hub(
            name="Suburban Hub",
            code="SH",
            address="Suburban Area",
            latitude="27.7200",
            longitude="85.3250",
            description="Suburban distribution hub",
            dealer=dealer2,
        )

        db.add_all([hub1, hub2])
        db.commit()

        # Create inventory
        inv1 = Inventory(
            dealer_id=dealer1.id,
            hub=hub1,
            brand=brand1,
            filled_quantity=1000,
            empty_quantity=50,
            reserved_quantity=100,
            damaged_quantity=10,
            low_stock_threshold=100,
        )
        inv2 = Inventory(
            dealer_id=dealer1.id,
            hub=hub1,
            brand=brand2,
            filled_quantity=800,
            empty_quantity=30,
            reserved_quantity=80,
            damaged_quantity=5,
            low_stock_threshold=80,
        )
        inv3 = Inventory(
            dealer_id=dealer2.id,
            hub=hub2,
            brand=brand1,
            filled_quantity=1200,
            empty_quantity=60,
            reserved_quantity=120,
            damaged_quantity=15,
            low_stock_threshold=120,
        )

        db.add_all([inv1, inv2, inv3])
        db.commit()

        print("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
