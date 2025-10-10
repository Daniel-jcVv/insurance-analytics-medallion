# Tests

## Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Make sure MinIO is running
docker-compose up -d

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=scripts --cov-report=term-missing
```

## What is tested

- **test_upload.py**: Integration tests for MinIO upload functionality
  - Connection to MinIO
  - Bucket creation
  - File upload and verification
  - File existence checks

## Test Philosophy

These are **integration tests**, not unit tests. They verify that:
- The upload scripts work with real MinIO instance
- Files are uploaded correctly
- Data integrity is maintained

For a portfolio project, this demonstrates:
- ✅ Understanding of testing in data pipelines
- ✅ Practical validation approach
- ✅ Quality assurance mindset

## Notes

- Tests use a separate bucket (`test-insurance-data`)
- Tests clean up after themselves
- MinIO must be running on localhost:9100
