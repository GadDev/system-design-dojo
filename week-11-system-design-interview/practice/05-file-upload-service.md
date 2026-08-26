# Practice 05 — Large File Upload Service 🟡

## Prompt

> Design a service for users to upload files up to 10 GB reliably.

## Requirement cards

- browser/mobile clients
- unreliable connections
- progress UI
- pause/resume
- private objects
- checksum validation
- 30-day staging cleanup

## Main lesson

```text
control plane vs data plane
```

A likely flow:

```text
Client → API → create upload session
Client =================> Object Storage
Client → API → complete upload
```

Questions:

- multipart size?
- parallel parts?
- stale upload cleanup?
- presigned URL expiry?
- duplicate completion?
- malware/media validation?
