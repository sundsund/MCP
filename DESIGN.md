# Dispute Resolution Scheduler Design

## Overview
This system is designed to handle healthcare claim disputes for multiple providers. It uses a configurable scheduler to manage tasks across 7 primary stream types, each with its own sub-stream operations.

## Architecture
- **Infrastructure**: AWS EKS (Elastic Kubernetes Service) for hosting the applications.
- **Messaging**: AWS MSK (Managed Streaming for Kafka) for high-volume message handling.
- **Database**: AWS Aurora PostgreSQL for persistent storage, using a schema-per-provider approach for multi-tenancy.
- **Security**: SASL/SCRAM or SASL/IAM for MSK authentication to ensure provider-level access control.

## Components
1. **Scheduler Service (Producer)**:
    - Built with Python.
    - Uses `APScheduler` for task scheduling.
    - Categorizes tasks into 7 stream types.
    - Produces messages to MSK topics.
2. **Worker Service (Consumer)**:
    - Consumes messages from MSK.
    - Implements sub-stream operations for each stream type.
    - Uses provider-specific schemas in Aurora PostgreSQL.
3. **Database Layer**:
    - Managed by SQLAlchemy.
    - Dynamic schema switching based on provider ID.

## Data Model
- `Provider`: Metadata about the healthcare providers.
- `Dispute`: Central entity for claim disputes.
- `StreamType`: Enumeration of the 7 primary streams.
- `SubStreamOperation`: Specific actions within a stream.

## Deployment
- Kubernetes manifests for EKS.
- MSK configuration with SASL enabled.
- Aurora PostgreSQL cluster.
