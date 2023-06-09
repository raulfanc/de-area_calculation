# Shape Calculator Challenge

The application should calculate the total area of all the shapes in the data set.
```json lines
{"type": "rectangle", "width": 5, "height": 10}
{"type": "triangle", "base": 2, "height": 3}
{"type": "circle", "radius": 4}
{"type": "rectangle", "width": 5, "height": 5}
```
## Assumptions
- how to approach software development
- what quality software looks like
- focus on highlighting in Data Engineering

## Objectives
To demonstrate not just technical ability but also the approach to software development, decision-making, problem-solving and attention to quality and details.

## Requirements
1. Develop a modular, maintainable application in Python, preferably using the Prefect framework and Apache Spark for data wrangling, parameterizing with Prefect, and parallelising the data extraction.

2. The application will ingest JSON data that represents various geometric shapes (currently rectangles, triangles, and circles, but the solution should be extensible for more shapes in the future).

3. The data can be provided in different formats, with potentially different key names for the shape properties.

4. The application should calculate and return the total area of all the shapes in the data set.

5. The solution should handle common issues with JSON data, including missing fields, unexpected values or types, and malformed JSON.

6. The solution should be unit-testable, preferably using the Pytest library for Python.

7. The application should handle parallel data extraction from multiple data sources. For the purpose of this challenge, the solution will be designed to handle API calls and load JSON files from an S3 bucket, but should be extensible to other data sources in the future.

8. Include documentation for the application, detailing the design choices, dependencies, how to run the application, and how to extend it for additional shapes and data sources.

9. The application's code should follow best practices for readability, maintainability, and performance.

10. Ensure the solution is scalable, meaning it can handle large volumes of data without a significant decrease in performance.

