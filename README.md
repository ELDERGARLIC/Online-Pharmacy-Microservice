# Online Pharmacy Microservice Project

<img width="865" alt="image" src="https://github.com/ELDERGARLIC/Online-Pharmacy-Microservice/assets/52277462/d717f303-7235-4b28-9328-812e768eedab">

## 1. Introduction and Project Overview

In our fast-evolving world, the healthcare sector must keep up with the pace of technology. Particularly, processes related to prescription medications require a user-friendly, scalable, and secure platform. Microservice architecture provides an ideal solution to efficiently manage and distribute drug treatments, making it more flexible and faster. With this vision in mind, we present our Online Pharmacy System, built using microservice architecture, aiming to redefine the process of purchasing prescription drugs and make our lives easier.

Our system focuses on providing users with easy and convenient access to prescription medications from the comfort of their homes, without any time or location constraints. This project is designed to simplify the lives of both patients and pharmacies. Our application first scans the contents of prescriptions, queries the inventories of nearby pharmacies, and verifies the availability of the required medications. Then, the medications are delivered to the buyer through a courier service. Patients can place orders from their homes without having to visit a physical pharmacy. Our system offers the convenience of purchasing medications online while providing fast solutions to patients' urgent medication needs.

The Online Pharmacy Application offers numerous benefits. For instance, it provides a solution for users who find physically buying specific medications or medical supplies embarrassing. Through online transactions, such situations remain private and confidential. Additionally, online pharmacies often offer more detailed information about medications, allowing users to have better insights into their prescribed drugs. Furthermore, it helps pharmacies extend their services to a broader customer base.

The Online Pharmacy Application is a significant need, considering the diversity of illnesses and the variety of ways people manage these conditions. Therefore, we believe that implementing this project is crucial for all patients and the entire healthcare sector.

## 2. Inspirations from Existing Projects

Our project takes inspiration from several existing projects. We researched and came up with the perfect solution.

## 3. Project Requirements

To realize this project, we determined the functional and non-functional requirements that this system demands. 

### 3.1 Functional Requirements

1. User Service: User registration and authentication (User Service).
2. Prescription Service: Uploading prescriptions and retrieving medication information (Prescription Service).
3. Order Service: Order creation and inventory update after order placement (Order Service).
4. Payment Service: Secure payment processing (Payment Service).
5. Inventory Service: Managing medication inventory (adding, updating, and deleting medications) (Inventory Service).

### 3.2 Non-Functional Requirements

1. Performance: The system should respond quickly and handle high user traffic efficiently.
2. Scalability: The system should be capable of scaling to accommodate increasing user numbers and growing databases.
3. Security: User and payment information should be processed and stored securely, using data encryption and secure connections.
4. Usability: The system should provide a user-friendly interface and easy navigation.
5. Loose Coupling: Each service should operate independently online and maintain loose coupling with others.
6. Maintainability: Each service should support the addition of new features and the correction of existing ones.
7. Database Management: Proper data backup and optimization of database performance.

## 4. Services

Each microservice operates independently online and communicates with other services. Loose coupling is maintained between the services to follow microservice architecture principles.

### 4.1 User Service

The User Service is the only service with which users directly interact. It also serves as the API gateway for our application. This service handles various requests, such as registering and signing in users. Passwords are tokenized for secure masking. The service interacts with the Prescription Service when users upload prescriptions.

### 4.2 Prescription Service

The Prescription Service is responsible for creating prescriptions and providing the necessary data for order creation. It communicates directly with the Order Service. This service handles requests to get all prescriptions, a specific prescription, or prescriptions of a particular user. It also allows the deletion of a prescription.

### 4.3 Order Service

The Order Service is responsible for order creation, updating the inventory after orders, and storing them in the database. It interacts with the Inventory Service to update the inventory based on the medication information. The service handles requests to get all orders, a specific order, or orders of a particular user. It also allows the deletion of an order.

### 4.4 Payment Service

The Payment Service handles payment approvals and updates the order status after approval. It stores payment approvals in the database. The service handles requests to get all payment approvals, a specific approval, or approvals of a particular user. It also allows the deletion of a payment approval.

### 4.5 Inventory Service

The Inventory Service manages the medication inventory. It handles requests to get all medications, a specific medication, add new medications, and update existing medication quantities in the inventory. The Inventory Service is used to update the inventory after an order is completed.

## 5. Project Architecture

The architecture of our project has been restructured to be simpler and more understandable than the initial design. The Prescription Service now directly communicates with the Order Service. These changes have resulted in cleaner, more understandable, and SOLID-compliant code development for our project.

### 5.1 Modules

- **User Service**: This microservice allows users to interact with the application and acts as the API gateway. It handles user registration, authentication, and user-related operations.
- **Prescription Service**: Responsible for creating and managing prescriptions, as well as providing essential data for order creation.
- **Order Service**: Handles order creation, inventory updates after orders, and storing orders in the database.
- **Payment Service**: Manages payment approvals and updates order statuses after approval.
- **Inventory Service**: Responsible for managing medication inventory, including adding, removing, and updating medication quantities.

### 6. Screenshots

Below are Postman screenshots showing interactions with our microservices:

<img width="769" alt="image" src="https://github.com/ELDERGARLIC/Online-Pharmacy-Microservice/assets/52277462/dda294a4-8ef5-4af9-9e6b-856917408666">

<img width="863" alt="image" src="https://github.com/ELDERGARLIC/Online-Pharmacy-Microservice/assets/52277462/90e9fd51-d80e-45de-ae00-cc9da2358535">

<img width="880" alt="image" src="https://github.com/ELDERGARLIC/Online-Pharmacy-Microservice/assets/52277462/831b0b32-ae7a-422d-b667-2279686970ad">




