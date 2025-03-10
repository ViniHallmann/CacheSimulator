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
