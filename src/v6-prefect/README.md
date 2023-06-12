# Prefect
**using Prefect to orchestrate workflow**

```bash
pip install -U "prefect==2.7.7"
```

- start Prefect server
```bash
prefect orion start
```

- run prefect script
```bash
python -m src.v6-prefect.prefect-pipeline
```

![](../../Pictures/Pasted%20image%2020230610212547.png)


## todo
1. **Improving Error Handling and Logging**: Currently, the script prints an error message when encountering invalid 
JSON but doesn't do much else with this information. One improvement could be to log this information to a file or a 
database for later analysis. This could be very useful for troubleshooting and improving the quality of the input data.
2. **Scaling data extraction with Spark**: can significantly speed up your data extraction.
