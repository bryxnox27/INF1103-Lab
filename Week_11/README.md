# INF1103 Week 11 Lab 9

This project extends the Week 10 inventory system with order discount strategies, a product factory, stricter product validation, and a CSV import that reports and skips invalid rows.

## Reused Week 10 files

The product hierarchy, supplier, inventory, order line, inventory data, and Docker setup carry forward from Week 10. `Order` now accepts a discount strategy, and product creation in the application goes through `ProductFactory`.

## Run locally

From this folder, run:

```text
python main.py
python -m unittest discover -s tests -v
```

Choose menu option 8 to import `products.csv`. The CSV format does not contain product weight or download size, so imported products use `0.0` for that type-specific field. Products added through the menu can include those details.

## Run with Docker

```text
docker build -t inf1103-week11 .
docker run --rm -it inf1103-week11
docker run --rm inf1103-week11 python -m unittest discover -s tests -v
```

The Docker image copies the application, CSV data, and tests so the same image can run the program or its test suite.

## Predict First notes

The accompanying worksheet gives a short thinking cue for each prediction and leaves space for personal predictions and reflections. Fill those in before running the matching code, then compare them with the recorded behavior.
