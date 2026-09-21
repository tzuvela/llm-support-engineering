# HDFS

Source: Apache Hadoop documentation
Primary reference: Hadoop 2.7.7 HDFS Users Guide
https://hadoop.apache.org/docs/r2.7.7/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html

## Overview

Hadoop Distributed File System (HDFS) is the primary distributed storage system used by Hadoop applications.

An HDFS cluster primarily consists of:

- NameNode
- DataNodes

The NameNode manages file system metadata.

DataNodes store the actual data.

Clients contact the NameNode for file metadata and file system operations, and perform actual file I/O with DataNodes.

## NameNode

The NameNode manages the file system namespace and metadata.

The NameNode is a central component of HDFS and maintains information about files and directories in the file system.

Clients communicate with the NameNode when they need file metadata or when they perform operations that modify the file system.

## DataNode

DataNodes store the actual data in HDFS.

A DataNode runs on a machine in the HDFS cluster and participates in storing and serving data.

The NameNode and DataNodes therefore have different responsibilities:

- NameNode: file system metadata and namespace management
- DataNode: storage of file data

## HDFS Client Leases

When an HDFS client opens a file for writing, HDFS uses a lease associated with the writer.

The client is responsible for renewing the lease periodically.

Lease renewal is associated with communication between the HDFS client and the NameNode.

If a lease is not renewed before it expires, the NameNode can consider the writer to have failed and perform lease recovery or otherwise close the file.

A lease-renewal failure therefore indicates that an HDFS client reported difficulty maintaining its lease.

The log message alone does not establish why lease renewal failed.

Possible explanations require further evidence from the incident and the surrounding system state.
