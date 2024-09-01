# Publisher-Subscriber Model using FastAPI and Decorator Pattern

This project demonstrates a Publisher-Subscriber model implemented using FastAPI and the decorator pattern. The system utilizes RabbitMQ for message passing, Docker for containerization, and a round-robin approach for distributing tasks among multiple subscribers.

## Getting Started

Follow the steps below to set up and run the application:

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Steps to Run

1. **Clone this repository**:

   ```bash
   git clone https://github.com/shaakib99/pubsub-fastapi.git
   cd pubsub-fastapi
   ```

2. **Run the Docker containers**:

   Use the following command to start all the necessary services:

   ```bash
   docker-compose up -d
   ```

3. **Send requests using Postman or a similar service**:

   Open Postman or any similar HTTP client to test the API.

4. **Send a request to the publisher**:

   Send a `GET` request to:

   ```
   http://localhost:8000
   ```

5. **Check the logs of Subscriber 1**:

   In the logs of Subscriber 1's container, you should see an output log like:

   ```
   Received data [x]: <message-content>
   ```

6. **Send another request**:

   Send another request to the same endpoint:

   ```
   http://localhost:8000
   ```

7. **Check the logs of Subscriber 2**:

   This time, the log will appear in the Subscriber 2 container, demonstrating the round-robin distribution of tasks.

### How It Works

- The system uses RabbitMQ to manage the message queue between the publisher and multiple subscribers.
- Each request sent to the publisher is pushed to the message queue.
- Subscribers consume messages from the queue using a round-robin approach, ensuring that tasks are evenly distributed among them.

### Additional Information

- The publisher is implemented using FastAPI.
- The decorator pattern is used to manage the routing and processing of messages efficiently.
- Subscribers are designed to log incoming messages to demonstrate task distribution.

Feel free to explore the code to understand the implementation details and modify it to suit your needs.

---

Happy Coding!
```
