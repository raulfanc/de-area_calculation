# start working on validations.
since we have checked the shape, we here to check the keys for each shape.


- Implement functionality to read, parse and validate JSON data. 
- Validation could include checking for necessary `keys` for the right data types. 
- Test this functionality with hard-coded JSON data.

```bash
python -m src.v3.area_cal_val    
```

![](../../Pictures/Pasted%20image%2020230610171628.png)


# todo

- shape and key done, need to validate value too

- Data Quality: If more shape types or keys are added, extend the validation function to handle those.

- API Interaction: If the JSON data is going to be fetched from an API in the future, a new layer of functionality would need to handle API interaction including rate limiting, error handling, pagination, authentication, and potentially API versioning.

- Data Consistency: If the source of data is subject to frequent changes, you will need to have a strategy for handling such updates, especially if you are persisting this data.

- Complex JSON Structure: If your application starts dealing with more complex JSON structures, your validation function might need to account for nested data.
