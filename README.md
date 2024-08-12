
# Picus Case

## Overview

It was very entertaining and instructive case for me. I started to work on the case by using CloudFormation to ensure the setup was as modular, maintainable, and shareable as possible. However, when time became limited, I shifted my focus to completing the remaining features. Unfortunately, some IAM roles and definitions in the CloudFormation YAML files are not fully up-to-date. 

## Table of Contents

- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Infrastructure](#infrastructure)
- [Application Deployment](#application-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring and Logging](#monitoring-and-logging)
- [Security](#security)
- [Testing](#testing)
- [Improvements](#improvements)

## Architecture

The application architecture is designed with the following key components:

1. **VPC Configuration**:
   - **Public Subnets**: Contain the Application Load Balancer (ALB).
   - **Private Subnets**: Host the application running on AWS Fargate within ECS.
   - **NAT Gateway**: Provides internet access to the instances in private subnets.

2. **Compute**:
   - **AWS Fargate**: Runs containerized applications in a serverless manner, handling provisioning and scaling automatically.
   - **AWS Lambda**: Used for lightweight, event-driven tasks, managed with the Serverless Framework.

3. **Networking**:
   - **Application Load Balancer (ALB)**: Distributes incoming traffic to the application running in private subnets, ensuring high availability and fault tolerance.

4. **Database**:
   - **DynamoDB**: A fully managed NoSQL database, used for storing application data with low latency and high scalability.

5. **Deployment**:
   - **AWS CodeDeploy**: Manages blue/green deployments, ensuring zero-downtime updates to the application.
   - **Serverless Framework**: Manages deployment and versioning of AWS Lambda functions.
   - **AWS ECR (Elastic Container Registry)**: Stores Docker images for the application, facilitating easy integration with AWS Fargate and the CI/CD pipeline.

## Tech Stack

- **Programming Language**: Python (used for both the main application and Lambda functions)
- **Infrastructure as Code**: AWS CloudFormation
- **Database**: AWS DynamoDB
- **Compute**: AWS Fargate, AWS Lambda
- **Container Registry**: AWS ECR
- **Networking**: VPC, Subnets (Public/Private), NAT Gateway, ALB
- **Deployment**: AWS CodeDeploy (Blue/Green), Serverless Framework
- **CI/CD**: GitHub Actions
- **Monitoring & Logging**: AWS CloudWatch
- **Security**: AWS IAM, Security Groups, VPC

## Infrastructure

### VPC and Networking

- **VPC**: Custom VPC with multiple subnets (public and private).
- **Subnets**:
  - **Public Subnets**: Host the ALB and NAT Gateway.
  - **Private Subnets**: Host the application within ECS on Fargate.
- **NAT Gateway**: Allows instances in private subnets to connect to the internet for updates and other outbound traffic.
- **Security Groups**: Define inbound and outbound traffic rules to secure the environment.

### Compute and Deployment

- **AWS Fargate**:
  - Runs the main application as a containerized service.
  - Handles scaling and maintenance automatically.
- **AWS Lambda**:
  - Manages lightweight, event-driven tasks like CRUD operations on DynamoDB.
  - Deployed using the Serverless Framework for efficient versioning and deployment.
- **AWS CodeDeploy**:
  - Manages blue/green deployments to ensure zero downtime during updates.
- **AWS ECR**:
  - Stores Docker images for the application, providing a secure and scalable registry that integrates seamlessly with ECS and Fargate.

### Database

- **DynamoDB**:
  - A highly available and scalable NoSQL database.
  - Used for storing persistent data with low-latency access.

## Application Deployment

### Blue/Green Deployment Strategy
The application uses AWS CodeDeploy to manage blue/green deployments. This approach ensures that new versions of the application are deployed to a separate environment (green) while the existing version (blue) continues to serve traffic. After verification, traffic is switched to the new version without any downtime.

### Serverless Framework for Lambda
Lambda functions are deployed using the Serverless Framework, which simplifies deployment, versioning, and rollback operations. The functions are primarily used for backend operations, such as handling DELETE requests for DynamoDB.

### Application Load Balancer (ALB)
The ALB is configured to distribute incoming HTTP/HTTPS traffic across the ECS tasks running in private subnets. This ensures that the application is highly available and can handle incoming traffic efficiently.

## CI/CD Pipeline

### GitHub Actions

A CI/CD pipeline is set up using GitHub Actions to automate the build, test, and deployment process:

- **Test**: Unit and integration tests are run to ensure code quality. The tests are written using `pytest` and are configured to run every time code is pushed to the `main` branch. The test suite includes both unit tests (to check individual functions and methods) and integration tests (to verify that different components of the application work together correctly).

- **Build & Deploy**: The Docker image is pushed to AWS ECR, and the application is deployed to ECS using AWS CodeDeploy for blue/green deployments(to zero downtime).

## Monitoring and Logging

### AWS CloudWatch

- **Alarms**: Set up for critical metrics such as CPU utilization, memory usage, and DynamoDB read/write capacity.
- **Logs**: CloudWatch Logs are used to capture and store logs from ECS tasks, Lambda functions, and the ALB.

## Security

### AWS IAM

- **Roles and Policies**: IAM roles are defined for each AWS service, ensuring that they have the necessary permissions while adhering to the principle of least privilege.

### VPC Security

- **Security Groups**: Security groups are configured to control inbound and outbound traffic at the instance level, ensuring that only authorized traffic can reach the application.

## Testing

### Unit and Integration Tests

Testing is a crucial part of ensuring that the application functions correctly. The test suite includes both unit and integration tests, focusing on validating the logic and the interactions between different components of the application.

#### Key Points:

-   **Libraries Used**:
    
    -   `pytest`: The main testing framework.
    -   `pytest-mock`: For mocking dependencies.
    -   `unittest.mock`: Used to create mock objects and isolate components during tests.
-   **Challenges**:
    -   **Import Path Issues**: Initially, there were challenges with importing modules from the `src` directory during testing. This was resolved by adjusting the `PYTHONPATH` in the CI/CD pipeline and modifying the `sys.path` directly within the test scripts.
-   **CI/CD Integration**:
    
    -   Tests are run automatically as part of the CI/CD pipeline using GitHub Actions. The pipeline ensures that code is tested before it is built and deployed, preventing faulty code from reaching production.


## Improvements

Reflecting on the development and deployment of this project,I identified several opportunities for improvement that could enhance the overall quality of the application.

1.  **Triggering Lambda with Load Balancer DNS**:
    
    -   **Current Situation**: The Lambda function for the DELETE `/picus/{key}` endpoint is currently triggered only through its API Gateway endpoint.
    -   **Improvement**: An enhancement would be to integrate the Lambda function with the Application Load Balancer (ALB). By configuring a target group within the ALB to trigger the Lambda function, all application endpoints could be uniformly accessible through the same ALB DNS. It would also improve security by centralizing traffic through a single load balancer, which can apply consistent security policies.

2. **Improved Logging and Monitoring**:

	-   **Current Situation**: AWS CloudWatch is used for logging and monitoring critical metrics such as CPU utilization and DynamoDB performance.
	-   **Improvement**: Enhancing the logging and monitoring setup to include distributed tracing (e.g., using AWS X-Ray) and more detailed application-level metrics could provide deeper insights into application performance and issues. This would allow for better root cause analysis and quicker resolution of problems.

3. **Restricting Public Access to Endpoints**:

	-   **Current Situation**: The public endpoints of the Application Load Balancer (ALB) and API Gateway are currently accessible to everyone on the internet, which poses a security risk.
	-   **Improvement**: To enhance security, these endpoints should be restricted to authorized users only. This could be achieved by creating an IAM role with specific policies that allow access to these endpoints. Alternatively, IAM users or groups with the necessary permissions could be created, and the access credentials or tokens could be shared with testers. This would ensure that only authorized testers have access to the application, significantly reducing the risk of unauthorized access and potential security breaches.

4. **Adding Linting Step for Every Code Push**:
    
    -   **Current Situation**: The current CI/CD pipeline primarily focuses on building, testing, and deploying the application. However, it lacks a linting step to enforce coding standards and detect potential issues before the code is merged or deployed.
    -   **Improvement**: Integrating a linting step in the GitHub Actions workflow for every code push to the branch would help maintain code quality and consistency.

5. **Creating a Development Environment to Isolate Production**:
    
    -   **Current Situation**: The application is currently deployed directly to the production environment. While this setup works, it poses a risk of introducing bugs or downtime in production due to untested changes.
    -   **Improvement**: Setting up a dedicated development environment that mirrors the production environment would allow for safer testing and validation of changes before they are pushed to production. This environment could be isolated from production and used for testing new features, bug fixes, and other updates. Once validated in the development environment, the changes could be promoted to production with greater confidence, reducing the risk of disruptions.