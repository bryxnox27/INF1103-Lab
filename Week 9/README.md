# Week 9 Inventory Management System

This folder extends the Week 8 inventory program with physical and digital products, abstract fulfillment behavior, and a shipping interface.

## Run with Docker

From this folder, build and run the app:

```powershell
docker build -t week9-inventory .
docker run -it --rm week9-inventory
```

The sample `inventory.json` contains both product types. Select **5. Save Inventory** to save changes. The image includes the sample JSON at build time; rebuild the image to include later host-side changes.

Shipping cost is calculated at $5.00 per kilogram in `PhysicalProduct.SHIPPING_RATE_PER_KG`.

## Submission notes

The lab handout asks for a screenshot of the Git and Docker workflow. Capture your own terminal after completing the workflow in your course repository. This folder contains the source, updated Mermaid UML diagram, and mixed-type persistence data; no Git push or workflow screenshot is included.

