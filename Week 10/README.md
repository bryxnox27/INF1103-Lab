# Week 10 Inventory Management System

This project extends Week 9 with suppliers, typed object relationships, and customer orders. It keeps the physical and digital product subclasses, the inventory menu, and JSON persistence.

## Run the application

From this directory, run:

```powershell
python main.py
```

Choose **7. Create Order** to create order lines from products already in the inventory. Orders calculate totals but do not change stock.

## Demonstrate Week 10 relationships

```powershell
python lab10_demo.py
```

The demo shows a supplier reference shared by products, transfer of a product between inventories, polymorphic product calls, and distinct order lines for one shared product.

## Run the submission checks

```powershell
python -m unittest -v test_lab10.py
```

The checks cover the Supplier association, Inventory aggregation, Order composition, type substitutability, shared Product behavior, and JSON compatibility with Week 9 records.

## Docker workflow

```powershell
docker build -t inf1103-week10 .
docker run --rm inf1103-week10 python -m unittest -v test_lab10.py
docker run --rm inf1103-week10 python lab10_demo.py
docker run --rm -it --mount "type=bind,source=$($PWD.Path)/inventory.json,target=/app/inventory.json" inf1103-week10
```

The last command mounts the local JSON file so saves remain in this project folder. To keep a workflow screenshot for submission, capture the build and run output in your terminal after running these commands.

## Git workflow

```powershell
git status
git add .
git diff --cached
git commit -m "Complete Week 10 object relationships"
git log --oneline -5
```

The Week 10 UML diagram is in [class_diagram.md](class_diagram.md). The prediction worksheet is `predict_first_notes.docx`; complete the prediction and observation fields as you work through the checks.
