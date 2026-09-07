# RECON-001 — Local HTTP Service

## Objective

Identify services exposed by the local cybersecurity laboratory.

## Scope

Target:
localhost

Port:
8000

## Methodology

The assessment started with service discovery
using Nmap and HTTP inspection using curl.

## Tools

- Nmap
- curl
- Python HTTP Server

## Finding

An HTTP service is exposed on TCP port 8000.

## Analysis

The service is intentionally exposed as part of the
local cybersecurity laboratory.

The open port itself is not considered a vulnerability.

## Risk

Informational

## Recommendation

In a production environment, unnecessary services
should not be exposed.

## Lessons Learned

Open ports should be treated as potential attack
surface, but an exposed service does not automatically
represent a vulnerability.
