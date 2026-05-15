import argparse

from cli import (
    list_inventory,
    get_inventory_item,
    search_product,
    import_product,
    update_inventory_item,
    delete_inventory_item,
)


def main():
    parser = argparse.ArgumentParser(description="Inventory Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List all inventory items")

    get_parser = subparsers.add_parser("get", help="Get one inventory item by ID")
    get_parser.add_argument("item_id", type=int)

    search_parser = subparsers.add_parser("search", help="Search OpenFoodFacts by barcode")
    search_parser.add_argument("barcode")

    import_parser = subparsers.add_parser("import", help="Import product from OpenFoodFacts")
    import_parser.add_argument("barcode")
    import_parser.add_argument("--price", type=float, required=True)
    import_parser.add_argument("--stock", type=int, required=True)

    update_parser = subparsers.add_parser("update", help="Update an inventory item")
    update_parser.add_argument("item_id", type=int)
    update_parser.add_argument("--price", type=float)
    update_parser.add_argument("--stock", type=int)
    update_parser.add_argument("--name")
    update_parser.add_argument("--brand")

    delete_parser = subparsers.add_parser("delete", help="Delete an inventory item")
    delete_parser.add_argument("item_id", type=int)

    args = parser.parse_args()

    if args.command == "list":
        list_inventory()

    elif args.command == "get":
        get_inventory_item(args.item_id)

    elif args.command == "search":
        search_product(args.barcode)

    elif args.command == "import":
        import_product(args.barcode, args.price, args.stock)

    elif args.command == "update":
        updates = {}

        if args.price is not None:
            updates["price"] = args.price

        if args.stock is not None:
            updates["stock"] = args.stock

        if args.name is not None:
            updates["name"] = args.name

        if args.brand is not None:
            updates["brand"] = args.brand

        if not updates:
            print("Please provide at least one field to update.")
            return

        update_inventory_item(args.item_id, updates)

    elif args.command == "delete":
        delete_inventory_item(args.item_id)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()