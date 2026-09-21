# Apache Hadoop YARN

## Overview

YARN separates resource management from application scheduling and monitoring.

The main components are:

- **ResourceManager (RM)** - the central authority for allocating cluster resources among applications.
- **NodeManager (NM)** - runs on each machine and manages containers, monitors resource usage, and reports information to the ResourceManager.
- **ApplicationMaster (AM)** - runs for an individual application and negotiates resources with the ResourceManager, then works with NodeManagers to execute and monitor the application's tasks.

## ResourceManager

The ResourceManager has two main components:

- **Scheduler** - allocates resources to running applications according to configured policies, queues and resource requirements.
- **ApplicationsManager** - accepts application submissions and manages the initial ApplicationMaster container, including restarting the ApplicationMaster container after failure.

The Scheduler allocates resources but does not itself monitor application status or guarantee that failed tasks will be restarted.

## NodeManager

A NodeManager is the per-machine agent in YARN.

It is responsible for:

- managing containers
- monitoring CPU, memory, disk and network usage
- reporting resource and container information to the ResourceManager and Scheduler

## ApplicationMaster

Each application has an ApplicationMaster.

The ApplicationMaster:

- negotiates resource containers from the ResourceManager
- tracks the status of those containers
- works with NodeManagers to execute and monitor application tasks

## Troubleshooting context

A log message indicating problems contacting the ResourceManager may indicate a communication problem between an application component and the ResourceManager.

The log alone does not establish the root cause.

Useful investigation areas include:

- ResourceManager availability
- network connectivity between components
- ResourceManager-related configuration
- application-side communication with the ResourceManager
- related warnings or errors occurring around the same time
