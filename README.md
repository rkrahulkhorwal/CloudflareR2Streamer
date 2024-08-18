# CloudflareR2Streamer

CloudflareR2Streamer is a Python utility for streaming file uploads to Cloudflare R2 storage directly from URLs. This tool allows you to efficiently transfer files from web sources to your R2 bucket without needing to download them to your local machine first.

## Features

- Stream uploads directly from URLs to Cloudflare R2
- Supports both small and large file uploads
- Uses multipart uploads for large files
- Provides detailed logging for troubleshooting
- Handles various error scenarios gracefully

## Requirements

- Python 3.6+
- `requests` library
- `boto3` library

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/rkrahulkhorwal/CloudflareR2Streamer.git
   cd CloudflareR2Streamer
   ```

2. Install the required dependencies:
   ```
   pip install requests boto3
   ```

## Configuration

Before using the script, you need to configure your Cloudflare R2 credentials. Open the `cloudflare_r2_streamer.py` file and replace the following placeholders with your actual R2 credentials:

- `<accountid>` in the `endpoint_url`
- `your_access_key_id`
- `your_secret_access_key`
- `your_bucket_name`

## Usage

Run the script using Python:

```
python cloudflare_r2_streamer.py
```

When prompted, enter the URL of the file you want to upload to your R2 bucket.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/rkrahulkhorwal/CloudflareR2Streamer/issues).


## Disclaimer

This tool is not officially associated with Cloudflare. Use it at your own risk and ensure you comply with Cloudflare's terms of service and any applicable laws and regulations.
