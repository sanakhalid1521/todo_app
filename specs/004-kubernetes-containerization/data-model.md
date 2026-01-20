# Data Model: Kubernetes Configuration for AI Chatbot Application

## Overview
This document defines the data models for Kubernetes resources required to deploy the AI Chatbot application. It includes the structure and relationships of Kubernetes objects needed for deployment.

## 1. Application Pod Model

### Definition
Represents the containerized application instances running in Kubernetes, containing both frontend and backend containers.

### Attributes
- **Name**: Unique identifier for the pod
- **Namespace**: Kubernetes namespace for the pod
- **Labels**: Key-value pairs for identification and selection
- **Annotations**: Additional metadata for the pod
- **Containers**: List of containers in the pod
  - Container Name
  - Image Reference
  - Ports
  - Environment Variables
  - Resource Limits and Requests
  - Health Checks (Liveness, Readiness, Startup Probes)
- **Volumes**: Storage volumes attached to the pod
- **Node Selector**: Constraints for pod placement
- **Affinity/Anti-Affinity**: Pod placement preferences

### Relationships
- One-to-Many: One Deployment manages many Pods
- Many-to-One: Many Pods belong to one Namespace

## 2. Service Discovery Model

### Definition
Kubernetes Services that enable communication between different application components.

### Attributes
- **Name**: Service name
- **Namespace**: Namespace where the service exists
- **Type**: Service type (ClusterIP, NodePort, LoadBalancer, ExternalName)
- **Selector**: Labels to select pods to serve traffic
- **Ports**: List of ports to expose
  - Port Number
  - Target Port
  - Protocol (TCP/UDP)
- **Session Affinity**: Session affinity configuration

### Relationships
- Many-to-Many: Services can select pods from multiple deployments
- One-to-Many: One Service can route to many Pods

## 3. Configuration Management Model

### Definition
Kubernetes ConfigMaps and Secrets that manage application settings and sensitive data.

### ConfigMap Attributes
- **Name**: ConfigMap name
- **Namespace**: Namespace where the ConfigMap exists
- **Data**: Key-value pairs of configuration data
- **Binary Data**: Binary configuration data

### Secret Attributes
- **Name**: Secret name
- **Namespace**: Namespace where the Secret exists
- **Type**: Secret type (Opaque, kubernetes.io/service-account-token, etc.)
- **Data**: Base64 encoded sensitive data
- **String Data**: Unencoded sensitive data (stored as base64 encoded in data)

### Relationships
- Many-to-Many: Deployments can mount multiple ConfigMaps and Secrets
- One-to-Many: One ConfigMap/Secret can be mounted by multiple Deployments

## 4. Network Policy Model

### Definition
Rules that control traffic flow between different parts of the application.

### Attributes
- **Name**: Network Policy name
- **Namespace**: Namespace where the policy applies
- **Pod Selector**: Selects pods to apply the policy to
- **Ingress Rules**: List of allowed inbound connections
  - From (sources)
  - Ports
  - Protocols
- **Egress Rules**: List of allowed outbound connections
  - To (destinations)
  - Ports
  - Protocols

### Relationships
- One-to-Many: One Network Policy can apply to many Pods
- Many-to-One: Many Network Policies can apply to one Pod

## 5. Deployment Model

### Definition
Defines how application pods are deployed and managed.

### Attributes
- **Name**: Deployment name
- **Namespace**: Namespace where the deployment exists
- **Replicas**: Desired number of pod replicas
- **Selector**: Label selector to identify pods
- **Template**: Pod template specification
- **Strategy**: Update strategy (RollingUpdate, Recreate)
- **Rollback Policy**: Rollback configuration
- **Revision History Limit**: Number of old ReplicaSets to retain

### Relationships
- One-to-Many: One Deployment manages many ReplicaSets (during updates)
- One-to-Many: One Deployment creates a Pod template that creates many Pods

## 6. Ingress Model

### Definition
Configures external access to services in a cluster, typically HTTP/HTTPS.

### Attributes
- **Name**: Ingress name
- **Namespace**: Namespace where the ingress exists
- **TLS**: TLS configuration
  - Hosts
  - Secret Name (for certificate)
- **Rules**: List of routing rules
  - Host
  - HTTP Paths
    - Path
    - Backend Service
    - Backend Service Port

### Relationships
- Many-to-Many: Ingress can route to multiple Services
- One-to-Many: One Ingress can have multiple rules

## 7. Horizontal Pod Autoscaler (HPA) Model

### Definition
Automatically scales the number of pods based on observed metrics.

### Attributes
- **Name**: HPA name
- **Namespace**: Namespace where the HPA exists
- **Scale Target Ref**: Reference to the resource to scale
- **Min Replicas**: Minimum number of replicas
- **Max Replicas**: Maximum number of replicas
- **Metrics**: List of metrics to scale on
  - Resource Metrics (CPU, Memory)
  - Custom Metrics
  - External Metrics

### Relationships
- One-to-One: One HPA scales one target resource (Deployment, ReplicaSet, etc.)

## 8. Persistent Volume Model (Not used in this application)

### Definition
Defines persistent storage in Kubernetes (not required for this application since it uses external NeonDB).

### Attributes
- **Name**: PV name
- **Capacity**: Storage capacity
- **Access Modes**: How the volume can be accessed
- **Volume Mode**: Filesystem or Block
- **Storage Class**: Storage class reference
- **Reclaim Policy**: What happens to the volume when released
- **Status**: Current status of the volume

## 9. Service Account Model

### Definition
Provides an identity for processes that run in a Pod.

### Attributes
- **Name**: Service Account name
- **Namespace**: Namespace where the SA exists
- **Automount Service Account Token**: Whether to auto-mount API tokens
- **Image Pull Secrets**: Secrets for pulling images from private registries

### Relationships
- Many-to-One: Many Pods can use the same Service Account
- One-to-Many: One Service Account can be used by many Pods

## 10. Resource Quota Model

### Definition
Provides constraints that limit aggregate resource consumption per namespace.

### Attributes
- **Name**: ResourceQuota name
- **Namespace**: Namespace where the quota applies
- **Hard Limits**: Hard limits for each resource
- **Scopes**: Set of filters to define a subset of scopes

### Relationships
- One-to-Many: One ResourceQuota applies to many resources in a namespace