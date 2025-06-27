# Data Processing & Transformation Framework

## Key Architectural Decisions

**Assumption:**
The current request is to handle relatively large files - the primary bottleneck is IO (reading and writing large files), the data transformation logic is not complex.

### 1. Generic Design

The framework is built around three key abstractions:

*   `DataReader`: Interface for reading data from a source.
*   `DataTransformer`: Interface for transforming data item.
*   `DataWriter`: Interface for writing data to a destination 

The `DataProcessFramework` class orchestrates the process. 
This design makes the framework modular, For example, to support CSV input, only need to create a new `CSVReader` class that inherits from `DataReader`.

### 2. Concurrency Model (Producer-Consumer)

To process multiple files efficiently, the framework implements a producer-consumer pattern using Python's built-in threading and queue capabilities.

*   **Producers (readers workers)**: Each input file is assigned to a thread from the pool. These threads read data, transform it, and put the results onto a shared Queue.
*   **Consumer (writer worker)**: Dedicated thread consumes transformed items from the queue, groups them into batches, and writes them to the destination.


**Tradeoff Considered**:

*   **Threading vs. Multiprocessing**: I chose threads because they are well suited for the IO-bound work. If the transformation logic were more complex, Multiprocessing would have been a better choice to leverage multiple CPU cores.

* **Single Writer Bottleneck**: The framework uses a single writer thread to ensure data integrity. The tradeoff is that this writer becomes a bottleneck, as all parallel processing must go through this writer. The overall application speed is limited by how fast this single thread can write to disk.

### 3. Memory Management

* **Reading** - Instead of loading entire JSON files into memory, the `JSONFileReader` uses the `ijson` library to parse the JSON iteratively. This approach use a minimal amount of memory instaed of lodaing the entire file to the memory.

* **Writing** - The writer worker consumes items from the queue and collects them into batches. The size of these batches is configurable, this is ensuring that only a limited number of transformed items are held in memory being written to disk. 

### 4. Data Integrity and Validation

* The framework uses Pydantic to validate data while reading. The input schema can be set to the reader, and each record will be validate against it.


### 5. `signInActivity` Data Structure
 
The `signInActivity` field is stored as a nested JSON object. This design was chosen because:

1. It separates different types of sign-in events into distinct objects for better data clarity.
2. Each sign-in type contains both `date_time` and `request_id` fields, provide the option to track about the properties of each sign-in type.
3. Easy schema updates if new sign-in activity types or fields are added in the future.

## Future Scalability Enhancements

### Multiple Cores
* Use separate processes to take advantage of multiple CPU cores.
* Another option is to decoupling only the transformation logic into a separate pool of worker processes.


### Multiple Servers

Two options:

1. **Microservices**:
    * Break the framework into independent microservices.
    * Replace the in memory Queue with message broker like Kafka in order to enable the components to communicate across a network.
        1. **Reader Service**: Reads files from a shared storage location and publishes messages containing the raw data to a raw-data topic.
        2. **Transformer Service**: consume the raw-data topic. performs the transformation logic and publishes the results to a transformed-data topic.
        3. **Writer Service**: consume the transformed-data topic, and writes them to the destination.
    * The services can scaled based on its workload.

2. **Controller/Worker Setup**
    * A central controller service would manage the list of files to be processed.
    * The Controller assigns a file to a single worker and manges the job progress of each worker.


## How to Run the Process

### Prerequisites

*   Python 3.13.5
*   [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/assaflv/data-processing-framework.git
    cd data-processing-framework
    ```

2.  **Initialize the project environment and install dependencies:**
    ```bash
    uv sync
    ```

4.  **Place data files:**
    Ensure your source JSON files are located in the `data/` directory.

### Execution

Run the main application script from the project's root directory:

```bash
uv run src/main.py
```

The transformed data will be saved in batches to the folder configurated in `destination_path`


### Tests

To run the tests:
```
uv run pytest
```
