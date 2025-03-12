# CacheSimulator

## Installation and Execution

### Using Docker

1. Build and start the containers:
    ```sh
    docker compose -f docker-compose.yml up -d --build
    ```

2. To execute commands inside the container:
    ```sh
    docker exec -it meu_app bash
    ```

3. Commands to run inside the container:
    - To display help for the main script:
        ```sh
        python main.py -h
        ```
    - To run tests:
        ```sh
        cd Tests/
        python test_validator.py
        ```
4. Running Individual Tests

    - To run a specific test example, use the following command, replacing `<test_number>` with the test number (e.g., 1, 2, 3, etc.):
        ```sh
        python test_validator.py <test_number>
        ```

### Using Python in local Machine

1. Go to root folder

2. Execute Simulation:
    ```
    python main.py <NSETS> <BSIZE> <ASSOC.> <SUBST.> <flagOut> <arquivoEntrada> <-d> (Optional)
    ```

3. Display help for the main script:
    ```
    python main.py -h
    ```

4. Execute test:
    ```
    cd Tests/
    python test_validator.py
    ```
